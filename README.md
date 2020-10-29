# To-do app
## About the application

This application is a web-browser-based to-do app, written in Python utilising the Flask web development framework. Data is stored in a Trello board.

## Config

When running locally, environment variables are read in from the `.env` file. You should populate this file with your own values, using the `.env.template` file as a template. (You should create the `.env` file if it doesn't already exist, and make sure it's never copied into source control.)

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

This application is containerised using Docker. There are 2 Docker images (each of which has a corresponding build command and run command):

- One image is for local development ('dev'). This runs the app using a Flask development server, which can be hot-reloaded (i.e. changes to the application code will feed through to the running application without needing to rebuild the Docker image).
- One image is for production ('prod'). This runs the app using a Gunicorn production-ready server, which cannot be hot-reloaded.

Below are some useful commands you can run to:

- Manage Docker containers (e.g. if you want to quickly remove all containers).
- Build Docker images and use them to create containers which run your application. 

There is also a shell script `buildAndRun.sh` stored in the root of this repository. This contains many of the commands seen below. You can comment out particular lines if you don't want to run certain containers. You can run this shell script from a bash terminal (e.g. Git Bash) using the command `source buildAndRun.sh`.

The commands:

- Remove all images: `docker image rm $(docker images -aq)`
- Stop all running containers: `docker stop $(docker container ls -aq)`
- Remove all stopped containers: `docker rm $(docker container ls -aq)`
- Build the local dev image: `docker build --target dev --tag=todo-app:dev .`
- Build the production image: `docker build --target prod --tag=todo-app:prod .`
- Run the local dev container from the built image: `docker run -d -p 5000:5000 --mount type=bind,source="$(pwd)"/app,target=/app/app/ --env-file .env todo-app:dev`
- Run the production container from the built image: `docker run -d -p 5000:5000 --env-file .env todo-app:prod`

You can chain these together into one line using a semicolon:

- Clean up (remove all containers): `docker stop $(docker container ls -aq); docker rm $(docker container ls -aq)`
- Clean up, build and run local dev container: `docker stop $(docker container ls -aq); docker rm $(docker container ls -aq); docker build --target dev --tag=todo-app:dev .; docker run -d -p 5000:5000 --mount type=bind,source="$(pwd)"/app,target=/app/app/ --env-file .env todo-app:dev`
- Clean up, build and run production container: `docker stop $(docker container ls -aq); docker rm $(docker container ls -aq); docker build --target prod --tag=todo-app:prod .; docker run -d -p 5000:5000 --env-file .env todo-app:prod`

You can also run the container in an interactive shell mode:

- Run local dev container in interactive mode: `docker run -it -p 5000:5000 --mount type=bind,source="$(pwd)"/app,target=/app/app/ --env-file .env todo-app:dev /bin/bash`
- Run production container in interactive mode: `docker run -it -p 5000:5000 --env-file .env todo-app:prod /bin/bash`


Once a container is running your application successfully you can view in your web browser at [`http://localhost:5000/`](http://localhost:5000/).