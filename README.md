# To-do app
## About the application

This application is a web-browser-based to-do app, written in Python utilising the Flask web development framework. Data is stored in a Trello board.

## Getting started

The project uses [Poetry](https://python-poetry.org/) to manage package dependencies. As specified in [poetry.toml](poetry.toml) it creates a virtual environment within the project repo. When e.g. running or testing the application, commands should be prefixed with `poetry run` as this runs the commands within the virtual environment. For example instead of running the application using `flask run`, use `poetry run flask run `. This will ensure the correct dependencies are available to the application.

## Config

When running locally, environment variables are read in from the `.env` file. You should populate this file with your own values, using the `.env.template` file as a template. (You should create the `.env` file if it doesn't already exist, and make sure it's never copied into source control.)

When running using Docker, environment variables are read in from the `.env` file by Docker at runtime. This file is not copied to the container, nor is it committed to the git repo, so you will need to create it if it doesn't exist. You can use `.env.template` as a template.

Environment variables include:
- Flask server configuration variables (these already have default values in `.env.template`).
    - FLASK_APP
    - FLASK_ENV
- Trello authorisation parameters (you can get these from https://trello.com/app-key).
    - AUTH_PARAMS_KEY
    - AUTH_PARAMS_TOKEN
- The ID of the Trello board used to store data.
    - BOARD_ID (you can easily find this by opening your Trello board of choice in a browser, adding `.json` to the end of the URL, and retrieving the first item in the resulting JSON data (e.g. `"id":"<your board ID will be visible here>"`)).

## Running the application

### Local debugging

You can run the application from the command line using `poetry run flask run` and then navigating to [`http://localhost:5000/`](http://localhost:5000/) to view the running app. You should run the application from the repo root.

### Running using Docker

This application is containerised using Docker. There are 2 Docker images:

- One image is for local development ('dev'). This runs the app using a Flask development server, which can be hot-reloaded (i.e. changes to the application code will feed through to the running application without needing to rebuild the Docker image).
- One image is for production ('prod'). This runs the app using a Gunicorn production-ready server, which cannot be hot-reloaded.

Below are some useful commands you can run to:

- Manage Docker containers (e.g. if you want to quickly remove all containers).
- Use Docker Compose to build and run Docker images/containers (i.e. to run the application).

Cleaning up:

- Remove all images: `docker image rm $(docker images -aq)`
- Stop all running containers: `docker stop $(docker container ls -aq)`
- Remove all stopped containers: `docker rm $(docker container ls -aq)`
- Clean up (remove all containers): `docker stop $(docker container ls -aq); docker rm $(docker container ls -aq)`
- Super clean up (remove all images and containers): `docker stop $(docker container ls -aq); docker rm $(docker container ls -aq); docker image rm $(docker images -aq)`

Running using regular Docker:

- Build the local dev image: `docker build --target dev --tag=todo-app:dev .`
- Build the production image: `docker build --target prod --tag=todo-app:prod .`
- Run the local dev container from the built image: `docker run -d -p 5000:5000 --mount type=bind,source="$(pwd)"/app,target=/app/app/ --env-file .env todo-app:dev`
- Run the production container from the built image: `docker run -d -p 5050:5000 --env-file .env todo-app:prod`
- Run local dev container in interactive mode: `docker run -it -p 5000:5000 --mount type=bind,source="$(pwd)"/app,target=/app/app/ --env-file .env todo-app:dev /bin/bash`
- Run production container in interactive mode: `docker run -it -p 5050:5000 --env-file .env todo-app:prod /bin/bash`

Running using Docker Compose:

- Build and run the dev version of the app: `docker-compose up --build --detach --remove-orphans todo-app-dev`
- Build and run the prod version of the app: `docker-compose up --build --detach --remove-orphans todo-app-prod`
- Build and run the dev version of the app in interactive mode (i.e. with an interactive shell): `docker-compose run --rm todo-app-dev /bin/bash`

Once a container is running your application successfully you can view in your web browser at:

- dev: [`http://localhost:5000/`](http://localhost:5000/)
- prod: [`http://localhost:5050/`](http://localhost:5050/)

## Testing the application

### Intro

The application is tested using [pytest](https://docs.pytest.org/en/stable/). Dependencies on pytest are managed via Poetry (like all other Python package dependencies), so you don't need to install pytest.

### Config

The end-to-end (E2E) tests use [Selenium](https://selenium-python.readthedocs.io/) to run. Selenium requires a browser-specific driver in order to run. These are listed [here](https://selenium-python.readthedocs.io/installation.html#drivers). This project is currently setup to use geckodriver, which is the the Firefox driver. Download the relevant version for you (listed [here](https://github.com/mozilla/geckodriver/releases)), unzip and place the executable either in the project repo root, or on your PATH. You'll also need to have Firefox installed.

### Running the tests

To run all tests, run `poetry run pytest`. You can also specify specific test folders, e.g.: `poetry run pytest tests_e2e`.

Adding the `-r` flag to the `pytest` command outputs some short test summary information. This flag takes multiple [options](https://docs.pytest.org/en/stable/usage.html#detailed-summary-report). It defaults to `-rfE` (info provided for failures and errors), but if you want info on all tests regardless of the result then you can use `-rA`.