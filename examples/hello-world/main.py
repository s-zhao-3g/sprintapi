from sprintapi import (
    SprintApiServer,
    api_route,
    get_mapping,
    Controller
)


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
