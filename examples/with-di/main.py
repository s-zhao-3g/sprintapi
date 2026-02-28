"""
Dependency injection example for Sprintapi.

This script shows how to:
- Define config, controller, and service types in a separate package.
- Register those types by importing the modules.
- Start the server so DI can resolve dependencies.

Run:
    python main.py

Then call:
    GET http://localhost/app/name

Note: `SprintApiServer` defaults to host `0.0.0.0` and port `80`.
"""

# Import modules so decorators register configuration, controller, and service types.
import demo.config
import demo.controller
import demo.manager

from sprintapi import SprintApiServer


def main():
    # Create and run the server; pass `port=8000` to change the default.
    server = SprintApiServer()
    server.run()


if __name__ == '__main__':
    main()
