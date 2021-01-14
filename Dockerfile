#### Base image ####

# A base image from which other images can be built.
FROM python:3.8.6-buster as base

# Install Poetry.
RUN pip3 install poetry==1.1.2

# Create dedicated application folder in image and move into it.
RUN mkdir /todo-app/
WORKDIR /todo-app/

# Copy dependency congiguration files from host system into a dedicated application folder.
COPY \
    # Dependency configuration files.
    poetry.lock \
    poetry.toml \
    pyproject.toml \
    # Copy them to the application folder.
    ./

# Install application dependencies.
RUN poetry install

# Copy source code files from host system into a dedicated application folder.
COPY ./application/ ./application/


#### Local development image ####

# Create an image used for local development.
FROM base AS dev

# Define commands to be run when container is started.
CMD [ "poetry", "run", "flask", "run", "--host=0.0.0.0" ]


#### Production image ####

# Create an image used for running the app in a production environment.
FROM base as prod

# Define commands to be run when container is started.
CMD [ "poetry", "run", "gunicorn", "--bind=0.0.0.0:5000", "--chdir", "./application", "app:create_app()" ]