# To-do app
## About the application

This application is a web-browser-based to-do app, written in Python utilising the Flask web development framework. The app runs on an Azure App Service, data is stored in an Azure Cosmos DB, and authentication/authorisation is managed using GitHub's OAuth web application flow and the Flask-Login package.

## Getting started

The project uses [Poetry](https://python-poetry.org/) to manage package dependencies. As specified in [poetry.toml](poetry.toml) it creates a virtual environment within the project repo. When e.g. running or testing the application, commands should be prefixed with `poetry run` as this runs the commands within the virtual environment. For example instead of running the application using `flask run`, use `poetry run flask run `. This will ensure the correct dependencies are available to the application.

## Config

When running locally, environment variables are read in from the `.env` file. You should populate this file with your own values, using the `.env.template` file as a template. (You should create the `.env` file if it doesn't already exist, and make sure it's never copied into source control.)

When running locally using Docker, environment variables are read in from the same `.env` file by Docker at runtime. This file is not copied to the container.

Environment variables include:
- Cosmos DB authorisation parameters.
    - COSMOS_USERNAME
    - COSMOS_PASSWORD
- Cosmos DB database details:
    - COSMOS_HOST
    - COSMOS_PORT
    - COSMOS_TODO_APP_DATABASE (the name of the database you want to store your data in - this database will be created if it doesn't already exist)
- Flask server configuration variables (some of these already have default values in `.env.template`).
    - FLASK_APP (defines the name of the Flask app)
    - FLASK_ENV (determines the Flask environment - if left blank, this defaults to 'production'.)
    - [FLASK_SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY)
- Flask-Login configuration variables:
    - LOGIN_DISABLED (if set to True, then Flask-Login won't force users to login)
    - ROLE_FOR_DEV_PURPOSES (a custom env var.. if LOGIN_DISABLED is set to True, then this env var will determine what role the user should be artificially assigned)
- GitHub OAuth app settings
    - GITHUB_CLIENT_ID (the client ID of the GitHub OAuth app you'll need to set up)
    - GITHUB_CLIENT_SECRET (the secret token of the GitHub OAuth app)
- OAuthLib
    - OAUTHLIB_INSECURE_TRANSPORT (if set to equal 1, then OAuth2 will be allowed over HTTP)

## Security

### Setting up

You will need to [create an OAuth app on GitHub](https://docs.github.com/en/developers/apps/creating-an-oauth-app) and set the 'Homepage URL' to be where you want to view your app running (this could be e.g. http://localhost:5000/ if you are running locally, or it could be the URL of your deployed Azure App Service). For the 'Authorization callback URL' choose the same URL, but append `login/callback` to the end, e.g. http://localhost:5000/login/callback. When setting up you should get a client ID and a secret token - these can be entered into your [.env](.env) file as the `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` env vars.

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

You can run the application from the command line using `poetry run flask run` and then navigating to http://localhost:5000/ to view the running app. You should run the application from the repo root.

### Running using Docker

Below are some useful commands you can use to build and run Docker images.

Running using regular Docker:

- Build the local dev image: `docker build --target dev --tag todo-app:dev .`
- Build the production image: `docker build --target prod --tag todo-app:prod .`
- Run the local dev container from the built image: `docker run -p 5000:5000 --mount type=bind,source="$(pwd)"/application/,target=/todo-app/application/ --env-file .env todo-app:dev`
- Run the production container from the built image: `docker run -p 5000:5000 --env-file .env todo-app:prod`
- Run local dev container in interactive mode: `docker run -it --entrypoint /bin/bash -p 5000:5000 --mount type=bind,source="$(pwd)"/application/,target=/todo-app/application/ --env-file .env todo-app:dev`
- Run production container in interactive mode: `docker run -it --entrypoint /bin/bash -p 5000:5000 --env-file .env todo-app:prod`

Running using Docker Compose:

- Build and run the dev version of the app: `docker-compose up --build --remove-orphans todo-app-dev`
- Build and run the prod version of the app: `docker-compose up --build --remove-orphans todo-app-prod`
- Run the dev version of the app in interactive mode (i.e. with an interactive shell): `docker-compose run --entrypoint /bin/bash --rm todo-app-dev`
- Run the prod version of the app in interactive mode (i.e. with an interactive shell): `docker-compose run --entrypoint /bin/bash --rm todo-app-prod`

Once a container is running your application successfully you can view in your web browser at http://localhost:5000/.

## Testing the application

### Intro

The application uses the [pytest](https://docs.pytest.org/en/stable/) framework. Dependencies on pytest are managed via Poetry (like all other Python package dependencies), so you don't need to install pytest.

### Dependencies

The end-to-end (E2E) tests use [Selenium](https://selenium-python.readthedocs.io/) to run. Selenium requires a browser-specific driver in order to run. These are listed [here](https://selenium-python.readthedocs.io/installation.html#drivers). This project is currently setup to use ChromeDriver, which is automatically installed/updated when the e2e tests are run. You'll need to ake sure Chrome is installed when running locally using `poetry run pytest`. When running the tests using Docker, Chrome is automatically installed in the test container.

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

In the final Travis build stage, the app is deployed to an [Azure App Service](https://azure.microsoft.com/en-gb/services/app-service/). You will be able to view the app at https://insert-your-app-name-here.azurewebsites.net/.

### Config

First, you will need to set up an integration between Travis and your GitHub account, which can be done from your Travis settings.

Second, included in the [.travis.yml](.travis.yml) file are the environment variables the application needs in order to run (making the [.env](.env) file visible to Travis would mean committing it to Git history, which would be insecure). You will need to update these with your own credentials once they exist (for your Azure App Service, your Azure Cosmos DB, Docker, and Slack).

Most of these credentials are sensitive. Where sensitive they need to be encrypted. The best way to do this is using Travis CLI's `encrypt` command - see documentation [here](https://docs.travis-ci.com/user/encryption-keys/).

Details on configuring Slack notifications (including setting up a new Travis-Slack integration) can be found [here](https://docs.travis-ci.com/user/notifications/#configuring-slack-notifications).

You will need to create an Azure Resource Group, and within it create an Azure App Service and an Azure Cosmos DB. This can be done using via the Azure portal (a browser-based GUI), using the Azure CLI, or via Visual Studio's GUI. 

Notes for setting up the Cosmos DB:
- Your Cosmos DB should be set up as a MongoDB (you will be given this option when setting it up).
- You'll get a Cosmos DB connection string, which you can use to populate the Cosmos DB environment variables in [.env](.env).

Notes for setting up the App Service:
- Choose 'Docker Container' in the 'Publish' field when setting it up. Then on the next screen enter the details of your container so that your App Service knows what container to use.
- You'll need to add all of your environment variables (except those relating to the App Service itself - see further down) to the App Service you create, which can be done via Settings > Configuration or by using the Azure CLI.
- You'll also need to set up continuous deployment - you can turn this on via Settings > Deployment Center > Settings tab. At the bottom of this screen you can retrieve your app's Webhook URL, which when sent a POST request will cause your App Service to re-pull the container image and restart the app.
- Your Webhook URL will be of the form `https://\$$AZURE_APP_SERVICE_NAME:$AZURE_APP_SERVICE_DEPLOYMENT_PASSWORD@$AZURE_APP_SERVICE_NAME.scm.azurewebsites.net/docker/hook"`. Make sure to get your Azure App Service name (you will have defined this when setting up the App Service, but of course you can get it directly from the Webhook URL) and your Azure App Service deployment password (get this from the Webhook URL). Then add these to your [.travis.yml](.travis.yml) file (make sure to encrypt the deployment password first!) You won't need to add these to your [.env](.env) file, nor to your App Service environment variables.