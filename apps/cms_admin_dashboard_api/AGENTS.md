# cms-admin-dashboard-api - REST API for CMS Admin Dashboard

This repo contains the REST API for CMS Admin Dashboard

# Coding guidelines

- Each endpoints in a controller should have its own handlers.
- Naming convention and location of the files

    |                    | Location Dir | File name               | File name example     | Class name             | Class name example |
    | ------------------ | ------------ | ----------------------- | --------------------- | ---------------------- | ------------------ |
    | **Controllers**    | controllers  | ends with `_controller` | example_controller.py | (none)                 | (none)             |
    | **Handlers**       | handlers     | ends with `_handler`    | example_handler.py    | ends with `Handler`    | ExampleHandler     |
    | **Request model**  | models       | ends with `_request`    | example_request.py    | ends with `Request`    | ExampleRequest     |
    | **Response model** | models       | ends with `_response`   | example_response.py   | ends with `Response`   | ExampleResponse    |
    | **Dependency**     | dependencies | ends with `_dependency` | example_dependency.py | ends with `Dependency` | ExampleDependency  |