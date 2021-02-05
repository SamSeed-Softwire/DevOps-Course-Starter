####################
#### Base image ####
####################

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
RUN poetry install --no-dev --no-root


######################################################
### Base image with application code copied across ###
######################################################

# Create an image which is the same as the base image but with the application code copied across.
FROM base as base-with-app-code

# Copy source code files from host system into a dedicated application folder.
COPY ./application/ ./application/


#################################
#### Local development image ####
#################################

# Create an image used for local development.
FROM base AS dev

# Define commands to be run when container is started.
ENTRYPOINT [ "poetry", "run", "flask", "run" ]
CMD [ "--host=0.0.0.0" ]


##########################
#### Production image ####
##########################

# Create an image used for running the app in a production environment.
FROM base-with-app-code as prod

# Define commands to be run when container is started.
CMD poetry run gunicorn --bind=0.0.0.0:$PORT --chdir ./application 'app:create_app()'


####################
#### Test image ####
####################

# Create an image used for running the app in a production environment.
FROM base-with-app-code as test

# Install Chrome
RUN \
    curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb &&\
    apt-get update &&\
    apt-get install ./chrome.deb -y &&\
    rm ./chrome.deb

# Copy test files from host system into a dedicated test folders.
COPY .env.test ./
COPY ./tests_e2e/ ./tests_e2e/
COPY ./tests_integration/ ./tests_integration/
COPY ./tests_unit/ ./tests_unit/

# Define commands to be run when container is started.
ENTRYPOINT ["poetry", "run", "pytest"]