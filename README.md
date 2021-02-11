# To-do app
## About the application

This application is a web-browser-based to-do app, written in Python utilising the Flask web development framework. Data is stored in a Trello board.

## Getting started

The project uses [Poetry](https://python-poetry.org/) to manage package dependencies. As specified in [poetry.toml](poetry.toml) it creates a virtual environment within the project repo. When e.g. running or testing the application, commands should be prefixed with `poetry run` as this runs the commands within the virtual environment. For example instead of running the application using `flask run`, use `poetry run flask run `. This will ensure the correct dependencies are available to the application.

## Config

When running locally, environment variables are read in from the `.env` file. You should populate this file with your own values, using the `.env.template` file as a template. (You should create the `.env` file if it doesn't already exist, and make sure it's never copied into source control.)

When running locally using Docker, environment variables are read in from the same `.env` file by Docker at runtime. This file is not copied to the container.

Environment variables include:
- Flask server configuration variables (these already have default values in `.env.template`).
    - FLASK_APP
    - FLASK_ENV
- Trello authorisation parameters (you can get these from https://trello.com/app-key).
    - AUTH_PARAMS_KEY
    - AUTH_PARAMS_TOKEN
- The ID of the Trello board used to store data.
    - BOARD_ID (you can easily find this by opening your Trello board of choice in a browser, adding `.json` to the end of the URL, and retrieving the first item in the resulting JSON data (e.g. `"id":"<your board ID will be visible here>"`)).

## Docker

This application can be run and tested using Docker. There are 3 Docker build stages:

- 'dev' is for building local development images. This runs the app using a Flask development server, which can be hot-reloaded (i.e. changes to the application code will feed through to the running application without needing to rebuild the Docker image).
- 'prod' is for building production images. This runs the app using a Gunicorn production-ready server, which cannot be hot-reloaded.
- 'test' is for building testing images.

Below are some useful commands you can run to manage Docker containers and images (e.g. if you want to quickly remove all containers)

Cleaning up:

- Remove all images: `docker image rm $(docker images -aq)`
- Stop all running containers: `docker stop $(docker container ls -aq)`
- Remove all stopped containers: `docker rm $(docker container ls -aq)`
- Clean up (remove all containers): `docker stop $(docker container ls -aq); docker rm $(docker container ls -aq)`
- Super clean up (remove all images and containers): `docker stop $(docker container ls -aq); docker rm $(docker container ls -aq); docker image rm $(docker images -aq); docker system prune`

## Running the application

### Local debugging

You can run the application from the command line using `poetry run flask run` and then navigating to [`http://localhost:5000/`](http://localhost:5000/) to view the running app. You should run the application from the repo root.

### Running using Docker

Below are some useful commands you can use to build and run Docker images.

Running using regular Docker:

- Build the local dev image: `docker build --target dev --tag todo-app:dev .`
- Build the production image: `docker build --target prod --tag todo-app:prod .`
- Run the local dev container from the built image: `docker run -p 5000:5000 --mount type=bind,source="$(pwd)"/application/,target=/todo-app/application/ --env-file .env todo-app:dev`
- Run the production container from the built image: `docker run -p 5050:5000 --env-file .env todo-app:prod`
- Run local dev container in interactive mode: `docker run -it --entrypoint /bin/bash -p 5000:5000 --mount type=bind,source="$(pwd)"/application/,target=/todo-app/application/ --env-file .env todo-app:dev`
- Run production container in interactive mode: `docker run -it --entrypoint /bin/bash -p 5050:5000 --env-file .env todo-app:prod`

Running using Docker Compose:

- Build and run the dev version of the app: `docker-compose up --build --remove-orphans todo-app-dev`
- Build and run the prod version of the app: `docker-compose up --build --remove-orphans todo-app-prod`
- Run the dev version of the app in interactive mode (i.e. with an interactive shell): `docker-compose run --entrypoint /bin/bash --rm todo-app-dev`
- Run the prod version of the app in interactive mode (i.e. with an interactive shell): `docker-compose run --entrypoint /bin/bash --rm todo-app-prod`

Once a container is running your application successfully you can view in your web browser at:

- dev: [`http://localhost:5000/`](http://localhost:5000/)
- prod: [`http://localhost:5050/`](http://localhost:5050/)

## Testing the application

### Intro

The application uses the [pytest](https://docs.pytest.org/en/stable/) framework. Dependencies on pytest are managed via Poetry (like all other Python package dependencies), so you don't need to install pytest.

### Dependencies

The end-to-end (E2E) tests use [Selenium](https://selenium-python.readthedocs.io/) to run. Selenium requires a browser-specific driver in order to run. These are listed [here](https://selenium-python.readthedocs.io/installation.html#drivers). This project is currently setup to use geckodriver, which is the the Firefox driver. Download the relevant version for you (listed [here](https://github.com/mozilla/geckodriver/releases)), unzip and place the executable either in the project repo root, or on your PATH. You'll also need to have Firefox installed.

### Running the tests locally
To run all tests locally, run `poetry run pytest`. You can also specify specific test folders, e.g.: `poetry run pytest tests_e2e`.

Adding the `-r` flag to the `pytest` command outputs some short test summary information. This flag takes multiple [options](https://docs.pytest.org/en/stable/usage.html#detailed-summary-report). It defaults to `-rfE` (info provided for failures and errors), but if you want info on all tests regardless of the result then you can use `-rA`.

### Running the tests with Docker

Below are some useful commands you can use to build and run Docker test images.

Running using regular Docker:

- Build the test image: `docker build --target test --tag todo-app:test .`
- Run all tests (using the built image): `docker run --env-file .env todo-app:test`
- Run specific tests (using the built image): e.g. `docker run --env-file .env todo-app:test tests_e2e`

Running using Docker Compose:

- Build and run the test version of the app (all tests): `docker-compose up --build --remove-orphans todo-app-test`
- Build and run the test version of the app (specific tests): e.g. `docker-compose up --build --remove-orphans todo-app-test tests_e2e`