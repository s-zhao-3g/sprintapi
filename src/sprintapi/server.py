import fastapi
import importlib.resources
import uvicorn

from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.staticfiles import StaticFiles
from typing import Optional

from .config import get_configuration_types
from .controller import get_controller_types
from .logging import get_sprintapi_logger
from .middleware import CorsMiddleware
from .middleware.error_handler import register_sprintapi_errors
from .service import get_service_types
from .utility.di import DependencyContainer


__all__ = ['SprintApiServer']


_logger = get_sprintapi_logger('SprintApiServer')
_static_dir = importlib.resources.files('sprintapi') / 'static'


class SprintApiServer(uvicorn.Server):
    def __init__(
            self,
            host: str = '0.0.0.0',
            port: int = 80,
            /,
            enable_docs: bool = False,
            app_name: str = None,
            version: str = None,
    ):
        super().__init__(config=uvicorn.Config(
            app=self._setup_app(app_name, version),
            host=host,
            port=port
        ))
        self._app_name = app_name
        self._app.add_middleware(CorsMiddleware)
        self._controller_types = get_controller_types()

        # component registration
        self._di_container = DependencyContainer()
        for c in get_configuration_types():
            self._di_container.register(c, c.load, is_singleton=True)
        for c in self._controller_types:
            self._di_container.register(c, c, is_singleton=True)

        service_types = get_service_types()
        for s in service_types:
            self._di_container.register(s, s, is_singleton=True)

        self._managed_services = self._di_container.resolve_with_order(service_types)

        # register error handlers
        register_sprintapi_errors(self._app)

        # bind controllers
        for c in self._controller_types:
            controller = self._di_container.resolve(c)
            router = controller.get_router()
            class_name = controller.__class__.__name__
            self._app.include_router(router)
            _logger.info(f'Bind controller {class_name} with route prefix "{router.prefix}".')

        # bind static files
        self._app.mount('/static', StaticFiles(directory=_static_dir), name='static')
        if enable_docs:
            self._app.get('/docs', include_in_schema=False)(self._swagger_ui_html)
            self._app.get('/redoc', include_in_schema=False)(self._redoc_ui_html)

    @property
    def app(self):
        return self._app

    async def startup(self, sockets = None):
        await self._pre_startup()
        await super().startup(sockets)

    async def shutdown(self, sockets = None):
        await self._pre_shutdown()
        await super().shutdown(sockets)
        await self._post_shutdown()

    def _redoc_ui_html(self):
        return get_redoc_html(
            openapi_url=self._app.openapi_url,
            title=f'{self._app_name} - Redoc' if self._app_name else 'Redoc',
            redoc_js_url='/static/redoc/redoc.standalone.js',
        )

    def _swagger_ui_html(self):
        return get_swagger_ui_html(
            openapi_url=self._app.openapi_url,
            title=f'{self._app_name} - Swagger UI' if self._app_name else 'Swagger UI',
            swagger_favicon_url='/static/swagger-ui/favicon-32x32.png',
            swagger_js_url='/static/swagger-ui/swagger-ui-bundle.js',
            swagger_css_url='/static/swagger-ui/swagger-ui.css',
        )

    async def _pre_startup(self):
        # init services
        for s in self._managed_services:
            await s.init()
        _logger.info('Managers init complete.')

        # start services
        for s in self._managed_services:
            await s.start()
        _logger.info('Managers start complete.')

    async def _pre_shutdown(self):
        pass

    async def _post_shutdown(self):
        for s in self._managed_services[::-1]:
            await s.stop()
        _logger.info('Managers stop complete.')

    def _setup_app(self, app_name: Optional[str], version: Optional[str]):
        extra_args = {}
        if app_name:
            extra_args['title'] = app_name
        if version:
            extra_args['version'] = version
        self._app = fastapi.FastAPI(docs_url=None, redoc_url=None, **extra_args)
        return self._app
