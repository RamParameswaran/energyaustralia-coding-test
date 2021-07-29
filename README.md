# energyaustralia-coding-test for Ram Parameswaran @ July 2021

This is a solution repo for the [Integration Engineer code test](https://eacp.energyaustralia.com.au/codingtest/integration).

## Table of Contents

1. [Installation](#installation)
1. [Commands](#commands)
1. [Development](#development)
1. [Testing](#testing)
1. [Swagger](#swagger)

## Installation

You will need [docker](https://docs.docker.com/engine/installation/) and [docker-compose](https://docs.docker.com/compose/install/).

First, clone the project:

```bash
$ git clone https://github.com/RamParameswaran/energyaustralia-coding-test.git
$ cd energyaustralia-coding-test
```

Then install dependencies and check that it works

```bash
$ make install      # Install the pip dependencies on the docker container
$ make start        # Run the container containing your local python server
```

If everything works, you should see the swagger documentation [here](http://localhost:8000/apidocs/).

The API runs locally on docker containers.

Server logs are logged to `./server.log`.

Note - you can change the data API base_url by setting the "DATA_API_BASE_URL" environment variable in the `environment.env` file.

## Commands

You can display availables make commands using `make`.

While developing, you will probably rely mostly on `make start`; however, there are additional scripts at your disposal:

| `make <script>` | Description                                             |
| --------------- | ------------------------------------------------------- |
| `make install`  | Install the pip dependencies on the server's container. |
| `make start`    | Run your local server in its own docker container.      |
| `make test`     | Run unit tests with pytest in its own container.        |

## Testing

To add a unit test, simply create a `test_*.py` file anywhere in `./test/`, prefix your test classes with `Test` and your testing methods with `test_`. Unittest will run them automaticaly.
You can run your tests in their own container with the command:

```bash
$ make test
```

## Swagger

API Documentation is available [here](http://localhost:8000/schema).
The Swagger UI is available [here](http://localhost:8000/apidocs).

## Thanks

- Thanks to [Jaime Buelta](https://github.com/jaimebuelta) for maintaining the https://github.com/jaimebuelta/django-docker-template repo under the MIT license.
