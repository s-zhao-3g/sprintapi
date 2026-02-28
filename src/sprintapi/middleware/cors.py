import fastapi

from starlette.middleware.base import BaseHTTPMiddleware


__all__ = ['CorsMiddleware']


class CorsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.method != 'OPTIONS':
            response = await call_next(request)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        return fastapi.Response(status_code=200, headers={
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Authorization, Content-Type',
            'Access-Control-Allow-Origin': '*',
        })
