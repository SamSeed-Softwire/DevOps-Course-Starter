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

This application is containerised using Docker. Here are some useful commands you can run to manage Docker containers, and of course build the Docker image and us it to create containers which run your application:<br>

Stop all running containers: `docker stop $(docker container ls -aq)`<br>
Remove all stopped containers: `docker rm $(docker container ls -aq)`<br>
Build the image: `docker build --tag=todo-app .`<br>
Create a container from the built image: `docker run -d -p 5000:5000 --env-file .env todo-app`<br>

You can chain these together into one line using a semicolon:

Remove all containers: `docker stop $(docker container ls -aq); docker rm $(docker container ls -aq)`<br>
Build and run: `docker build --tag=todo-app .; docker run -d -p 5000:5000 --env-file .env todo-app`<br>
Remove all containers, then build and run: `docker stop $(docker container ls -aq); docker rm $(docker container ls -aq); docker build --tag=todo-app .; docker run -d -p 5000:5000 --env-file .env todo-app`<br>

Once a container is running your application successfully you can view in your web browser at [`http://localhost:5000/`](http://localhost:5000/).