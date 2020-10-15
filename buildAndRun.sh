### Initial cleanup

# Stop all running containers.
docker stop $(docker container ls -aq)

# Remove all stopped containers.
docker rm $(docker container ls -aq)


### Build

# Build dev image
docker build --target dev --tag=todo-app:dev .

# Build prod image
docker build --target prod --tag=todo-app:prod .


### Run

## Non-interactive

# Run non-interactive (dev)
#docker run -d -p 5000:5000 --mount type=bind,source="$(pwd)"/app,target=/app/app/ --env-file .env todo-app:dev

# Run non-interactive (prod)
#docker run -d -p 5000:5000 --env-file .env todo-app:prod

## Interactive (currently haven't worked out how to enter interactive mode when running this shell script on Windows)

# Run interactive (dev)
#docker run -it -p 5000:5000 --mount type=bind,source="$(pwd)"/app,target=/app/app/ --env-file .env todo-app:dev /bin/bash

# Run interactive (prod)
#docker run -it -p 5000:5000 --env-file .env todo-app:prod /bin/bash