# Sprintapi

Sprintapi is a small FastAPI-based framework that adds decorator-driven controllers,
a lightweight dependency injection container, and simple config/service lifecycles.

## Features

- Controller classes with route decorators (`@api_route`, `@get_mapping`, etc.).
- DI container that resolves constructor dependencies by type hints.
- Configuration models loaded from environment variables.
- Service lifecycle hooks (`init`, `start`, `stop`).
- Optional built-in Swagger UI and Redoc endpoints.

## Requirements

- Python 3.12+

## Install (editable)

```bash
pip install -e .
```

## Quick start

```python
# main.py

from sprintapi import SprintApiServer, api_route, get_mapping, Controller


@api_route('/simple')
class SimpleController(Controller):
    @get_mapping('hello')
    async def hello(self):
        return 'Hello, World!'


def main():
    server = SprintApiServer()
    server.run()


if __name__ == '__main__':
    main()
```

Run it:

```bash
python main.py
```
This runs a web server listening on `http://localhost:80`.
Then open `http://localhost/simple/hello` in your browser, you will see:
```
Hello, World!
```

## With Dependency Injection

```bash
> cd examples/with-di
> export APP_NAME="My Demo"
> python main.py
```

Then open:

- `GET http://localhost/app/name`

This example shows:

- `Configuration` reading from env vars via field aliases.
- `Service` registered with `@service` and injected into a `Controller`.

## API docs UI

Enable built-in docs with `enable_docs=True` when creating the server:

```python
from sprintapi import SprintApiServer

server = SprintApiServer(enable_docs=True, app_name="Sprintapi", version="0.1.0")
server.run()
```

Then open:

- `http://localhost/docs` (Swagger UI)
- `http://localhost/redoc` (Redoc)

## Project layout

- `src/sprintapi/` core package
- `examples/hello-world/` minimal controller example
- `examples/with-di/` DI + config + service lifecycle example

## License

MIT. See `LICENSE`.
