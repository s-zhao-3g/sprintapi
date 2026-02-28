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
pip install sprintapi
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

Then open `http://localhost/app/name` in your browser and you will see:
```
This app is My Demo
```

## License

MIT. See `LICENSE`.
