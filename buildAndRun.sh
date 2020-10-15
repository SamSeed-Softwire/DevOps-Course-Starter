### Initial cleanup

# Stop all running containers.
docker stop $(docker container ls -aq)

# Remove all stopped containers.
docker rm $(docker container ls -aq)


### Build only

# Build dev image
#docker build --target dev --tag=todo-app:dev .

# Build prod image
#docker build --target prod --tag=todo-app:prod .


### Build and run

## Non-interactive

# Run non-interactive (dev)
#docker build --target dev --tag=todo-app:dev .; docker run -d -p 5000:5000 --env-file .env todo-app:dev

# Run non-interactive (prod)
docker build --target prod --tag=todo-app:prod .; docker run -d -p 5000:5000 --env-file .env todo-app:prod


### Run only

## Interactive

# Run interactive (dev) with mount
#docker run -it -p 5000:5000 --env-file .env --mount type=bind,src="$pwd",dst=/app2 todo-app:dev /bin/bash

# Run interactive (dev)
#docker run -it -p 5000:5000 --env-file .env todo-app:dev /bin/bash