"""
Example of using SprintApi with dependency injection.
The dependencies are defined in the `demo` package, and the server is created and run in the `main` function.
"""

# Make sure to import the modules so that interpreter read the definitions

import demo.config
import demo.controller
import demo.manager

from sprintapi import SprintApiServer


def main():
    server = SprintApiServer()
    server.run()


if __name__ == '__main__':
    main()
