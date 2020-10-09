FROM python:3.8.6-buster

# Install Poetry.
RUN pip3 install poetry==1.1.2

# Copy necessary files from host system into a dedicated application folder.
RUN mkdir /app/
WORKDIR /app/

COPY templates/ templates/
COPY \
    # Application scripts.
    app.py \
    flask_config.py \
    item.py \
    session_items.py \
    trello_functions.py \
    viewModel.py \
    # Dependency configuration files.
    poetry.lock \
    poetry.toml \
    pyproject.toml \
    # Copy them to the application folder.
    ./

# Install application dependencies.
RUN poetry install

EXPOSE 5000

# Define commands to be run when container is started.
CMD [ "poetry", "run", "flask", "run", "--host=0.0.0.0" ]