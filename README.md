# To-do app
## About the application

This application is a web-browser-based to-do app, written in Python utilising the Flask web development framework. Data is stored in a MongoDB database, and authentication/authorisation is managed using GitHub's OAuth web application flow and the Flask-Login package.

## Getting started

The project uses [Poetry](https://python-poetry.org/) to manage package dependencies. As specified in [poetry.toml](poetry.toml) it creates a virtual environment within the project repo. When e.g. running or testing the application, commands should be prefixed with `poetry run` as this runs the commands within the virtual environment. For example instead of running the application using `flask run`, use `poetry run flask run `. This will ensure the correct dependencies are available to the application.

## Config

When running locally, environment variables are read in from the `.env` file. You should populate this file with your own values, using the `.env.template` file as a template. (You should create the `.env` file if it doesn't already exist, and make sure it's never copied into source control.)

When running locally using Docker, environment variables are read in from the same `.env` file by Docker at runtime. This file is not copied to the container.

Environment variables include:
- Flask server configuration variables (these already have default values in `.env.template`).
    - FLASK_APP
    - FLASK_ENV
- Flask-Login configuration variables:
    - LOGIN_DISABLED (if set to True, then Flask-Login won't force users to login)
    - ROLE_FOR_DEV_PURPOSES (a custom env var.. if LOGIN_DISABLED is set to True, then this env var will determine what role the user should be artificially assigned)
- GitHub OAuth app settings
    - GITHUB_CLIENT_ID (the client ID of the GitHub OAuth app you'll need to set up)
    - GITHUB_CLIENT_SECRET (the secret token of the GitHub OAuth app)
- MongoDB authorisation parameters.
    - MONGO_USERNAME
    - MONGO_PASSWORD
- MongoDB database details:
    - MONGO_HOST
    - MONGO_TODO_APP_DATABASE (the name of the database you want to store your data in - this database will be created if it doesn't already exist)
- OAuthLib
    - OAUTHLIB_INSECURE_TRANSPORT (if set to equal 1, then OAuth2 will be allowed over HTTP)

## Security

### Setting up

You will need to [create an OAuth app on GitHub](https://docs.github.com/en/developers/apps/creating-an-oauth-app) and set the 'Homepage URL' to be where you want to view your app running (this could be e.g. http://localhost:5000/ if you are running locally, or it could be the URL of your deployed Heroku app). For the 'Authorization callback URL' choose the same URL, but append `login/callback` to the end, e.g. http://localhost:5000/login/callback. When setting up you should get a client ID and a secret token - these can be entered into your [.env](.env) file as the `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` env vars.

### What you'll see

Once the application is running (see sections below), authentication/authorisation may be invoked depending on the config you have chosen.

If the env var LOGIN_DISABLED is *not* set to true, the Python package Flask-Login will force you to log in. It invokes the [GitHub OAuth web application flow](https://docs.github.com/en/developers/apps/authorizing-oauth-apps) in order to do this.

Once you are logged in with GitHub, the application will store your user details in the MongoDB database defined in your [.env](.env) file. The details it will store are:
- Your GitHub ID
- Your role (reader, writer or admin)
Your role will be set automatically the first time you log in. If there are no other users stored in the database, you'll be assigned the role of admin. If there are other users stored in the database, you'll be assigned the role of reader. Within the app, only admins can change users' roles, and admins can't change their own roles.

If the env var LOGIN_DISABLED is set to true, you will not be forced to log in. To manually decide what role you want to be, change the ROLE_FOR_DEV_PURPOSES env var, e.g. set it to equal "writer" if you want to automatically be granted writer permissions.

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

## CI / CD

### Intro

The application uses [Travis CI](https://www.travis-ci.com/), integrated with GitHub. When a pull request is created or updated, Travis builds the app and tests it. See [.travis.yml](.travis.yml) for how this works. Build status notifications are sent to Slack and via email.

In the final Travis build stage, the app is deployed to [Heroku](https://www.heroku.com/home). You will be able to view the app at https://insert-your-app-name-here.herokuapp.com/.

### Config

First, you will need to set up an integration between Travis and your GitHub account, which can be done from your Travis settings.

Second, included in the [.travis.yml](.travis.yml) file are the environment variables the application needs in order to run (making the [.env](.env) file visible to Travis would mean committing it to Git history, which would be insecure). You will need to update these with your own credentials (for Docker, MongoDB, Heroku and Slack).

Most of these credentials are sensitive. Where sensitive they need to be encrypted. The best way to do this is using Travis CLI's `encrypt` command - see documentation [here](https://docs.travis-ci.com/user/encryption-keys/).

Details on configuring Slack notifications (including setting up a new Travis-Slack integration) can be found [here](https://docs.travis-ci.com/user/notifications/#configuring-slack-notifications).

You will need to create a Heroku app, which can be done using Heroku's web interface or the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli). The app will be given a name (which you'll seee). Set the HEROKU_APP_NAME environment variable in your [.travis.yml](.travis.yml) to be this name.

You will also need to add the environment variables stored in your [.env](.env) file as 'config vars' to your Heroku app. That can be done from the browser in the app's settings, or by using the Heroku CLI. For example ``heroku config:set `cat .env | grep AUTH_PARAMS_KEY` `` stores the `AUTH_PARAMS_KEY` environment variable as a config var in Heroku.
