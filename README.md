# SprintAPI Framework

A lightweight FastAPI-based framework that can be used like Spring Boot, with built-in dependency injection and lifecycle management.

## Core features
- **Configuration via environment variables** over config file,
    which is friendly to containerized deployments and 12-factor apps;
- **Built-in dependency injection**, which enables IoC and better handles dependency management for larger apps;
- **Controller-based API design**, which is more intuitive for developers coming from other languages;
- **Lifecycle hooks** called on same event loop as the server, and are called in dependency order;

## Requirements

- Python 3.12+

## Install (editable)

```bash
pip install -e .
```

## Quick start

Below is a minimal example of a controller exposing a single GET endpoint.

```python
# main.py

from sprintapi import SprintApiServer, api_route, get_mapping, Controller


@api_route('/simple')
class SimpleController(Controller):
    """A minimal controller exposing a single GET endpoint."""

    @get_mapping('hello')
    async def hello(self):
        """Return a simple greeting."""
        return 'Hello, World!'


def main():
    # Create and run the server; pass `port=8000` to change the default.
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
