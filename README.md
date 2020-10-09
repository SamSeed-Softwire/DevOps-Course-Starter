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

This application is containerised using Docker. Here are some useful commands you can run to manage Docker containers, and of course build the Docker image and us it to create containers which run your application:

Stop all running containers: `docker stop $(docker container ls -aq)`
Remove all stopped containers: `docker rm $(docker container ls -aq)`
Build the image: `docker build --tag=todo-app .`
Create a container from the built image: `docker run -d -p 5000:5000 --env-file .env todo-app`

You can chain these together into one line using a semicolon:

Remove all containers: `docker stop $(docker container ls -aq); docker rm $(docker container ls -aq)`
Build and run: `docker build --tag=todo-app .; docker run -d -p 5000:5000 --env-file .env todo-app`
Remove all containers, then build and run: `docker stop $(docker container ls -aq); docker rm $(docker container ls -aq); docker build --tag=todo-app .; docker run -d -p 5000:5000 --env-file .env todo-app`

Once a container is running your application successfully you can view in your web browser at [`http://localhost:5000/`](http://localhost:5000/).