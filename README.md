# To-do app
## About the application

This application is a web-browser-based to-do app, written in Python utilising the Flask web development framework. Data is stored in a Trello board.
<br><br>

## Config

Environment variables are read in from the `.env` file by Docker at runtime. This file is not copied to the container, nor is it committed to the git repo, so you will need to create it if it doesn't exist. You can use `.env.template` as a template.

Environment variables include:
- Flask server configuration variables.
- A secret key, necessary for using the `session` object in Flask. A good secret key can easily be generated using the following Python command: `python -c 'import os; print(os.urandom(16))'`. Unsurprisngly this key should be kept secret!
- Trello authorisation parameters
<br><br>

## Running the application

This application is containerised using Docker. There are 2 Docker images:

- One image is for local development ('dev'). This runs the app using a Flask development server, which can be hot-reloaded (i.e. changes to the application code will feed through to the running application without needing to rebuild the Docker image).<br>
- One image is for production ('prod'). This runs the app using a Gunicorn production-ready server, which cannot be hot-reloaded.<br>

Below are some useful commands you can run to:

- Manage Docker containers (e.g. if you want to quickly remove all containers).<br>
- Use Docker Compose to build and run Docker images/containers (i.e. to run the application).

Cleaning up:

- Remove all images: `docker image rm $(docker images -aq)`<br>
- Stop all running containers: `docker stop $(docker container ls -aq)`<br>
- Remove all stopped containers: `docker rm $(docker container ls -aq)`<br>
- Clean up (remove all containers): `docker stop $(docker container ls -aq); docker rm $(docker container ls -aq)`<br>
- Super clean up (remove all images and containers): `docker stop $(docker container ls -aq); docker rm $(docker container ls -aq); docker image rm $(docker images -aq)`<br>

Running the app:

- Build and run the dev version of the app: `docker-compose up --detach --remove-orphans todo-app-dev`<br>
- Build and run the prod version of the app: `docker-compose up --detach --remove-orphans todo-app-prod`<br>
- Build and run the dev version of the app in interactive mode (i.e. with an interactive shell): `docker-compose run --rm todo-app-dev /bin/bash`<br>

Once a container is running your application successfully you can view in your web browser at:

- dev: [`http://localhost:5000/`](http://localhost:5000/)
- prod: [`http://localhost:5050/`](http://localhost:5050/)