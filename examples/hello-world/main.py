"""
Hello World example for SprintAPI.

This script shows how to:
- Define a controller with a class-level route prefix.
- Register a GET handler with a method-level route.
- Start the SprintAPI server with default settings.

Run:
    python main.py

Then call:
    GET http://localhost/simple/hello

Note: `SprintApiServer` defaults to host `0.0.0.0` and port `80`.
"""

from sprintapi import (
    SprintApiServer,
    api_route,
    get_mapping,
    Controller
)


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
