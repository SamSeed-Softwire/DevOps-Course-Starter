# To-do app
## About the application

This application is a web-browser-based to-do app, written in Python utilising the Flask web development framework. Data is stored in a Trello board.
<br><br>

## Config

Environment variables are read in from the `.env` file by Docker at runtime (using the --env-file option). This file is not copied to the container, nor is it committed to the git repo, so you will need to create it if it doesn't exist. You can use `.env.template` as a template.

Environment variables include:
- Flask server configuration variables.
- A secret key, necessary for using the `session` object in Flask. A good secret key can easily be generated using the following Python command: `python -c 'import os; print(os.urandom(16))'`. Unsurprisngly this key should be kept secret!
- Trello authorisation parameters
<br><br>

## Running the application

This application is containerised using Docker. There are 2 Docker images (each of which has a corresponding build command and run command):

- One image is for local development ('dev'). This runs the app using a Flask development server, which can be hot-reloaded (i.e. changes to the application code will feed through to the running application without needing to rebuild the Docker image).<br>
- One image is for production ('prod'). This runs the app using a Gunicorn production-ready server, which cannot be hot-reloaded.<br>

Below are some useful commands you can run to:

- Manage Docker containers (e.g. if you want to quickly remove all containers).<br>
- Build Docker images and use them to create containers which run your application. 

There is also a shell script `buildAndRun.sh` stored in the root of this repository. This contains many of the commands seen below. You can comment out particular lines if you don't want to run certain containers. You can run this shell script from a bash terminal (e.g. Git Bash) using the command `source buildAndRun.sh`.

The commands:

- Stop all running containers: `docker stop $(docker container ls -aq)`<br>
- Remove all stopped containers: `docker rm $(docker container ls -aq)`<br>
- Build the local dev image: `docker build --target dev --tag=todo-app:dev .`<br>
- Build the production image: `docker build --target prod --tag=todo-app:prod .`<br>
- Run the local dev container from the built image: `docker run -d -p 5000:5000 --mount type=bind,source="$(pwd)"/app,target=/app/app/ --env-file .env todo-app:dev`<br>
- Run the production container from the built image: `docker run -d -p 5000:5000 --env-file .env todo-app:prod`<br>

You can chain these together into one line using a semicolon:

- Clean up (remove all containers): `docker stop $(docker container ls -aq); docker rm $(docker container ls -aq)`<br>
- Clean up, build and run local dev container: `docker stop $(docker container ls -aq); docker rm $(docker container ls -aq); docker build --target dev --tag=todo-app:dev .; docker run -d -p 5000:5000 --mount type=bind,source="$(pwd)"/app,target=/app/app/ --env-file .env todo-app:dev`<br>
- Clean up, build and run production container: `docker stop $(docker container ls -aq); docker rm $(docker container ls -aq); docker build --target prod --tag=todo-app:prod .; docker run -d -p 5000:5000 --env-file .env todo-app:prod`<br>

You can also run the container in an interactive shell mode:

- Run local dev container in interactive mode: `docker run -it -p 5000:5000 --mount type=bind,source="$(pwd)"/app,target=/app/app/ --env-file .env todo-app:dev /bin/bash`<br>
- Run production container in interactive mode: `docker run -it -p 5000:5000 --env-file .env todo-app:prod /bin/bash`<br>


Once a container is running your application successfully you can view in your web browser at [`http://localhost:5000/`](http://localhost:5000/).