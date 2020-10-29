#### Base image ####

# A base image from which other images can be built.
FROM python:3.8.6-buster as base

# Install Poetry.
RUN pip3 install poetry==1.1.2

# Copy necessary files from host system into a dedicated application folder.
RUN mkdir /app/
WORKDIR /app/

COPY \
    # Dependency configuration files.
    poetry.lock \
    poetry.toml \
    pyproject.toml \
    # Copy them to the application folder.
    ./

# Install application dependencies.
RUN poetry install

COPY ./app/ ./app/

WORKDIR /app/app/

# Document what port should be exposed by the container when running.
EXPOSE 5000


#### Local development image ####

# Create an image used for local development.
FROM base AS dev

# Define commands to be run when container is started.
CMD [ "poetry", "run", "flask", "run", "--host=0.0.0.0" ]


#### Production image ####

# Create an image used for running the app in a production environment.
FROM base as prod

# Define commands to be run when container is started.
CMD [ "gunicorn", "--bind=0.0.0.0:5000", "app:app" ]