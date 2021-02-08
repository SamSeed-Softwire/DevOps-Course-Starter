# To-do app
## About the application

This application is a web-browser-based to-do app, written in Python utilising the Flask web development framework. Data is stored in a Trello board.

## Getting started

The project uses [Poetry](https://python-poetry.org/) to manage package dependencies. As specified in [poetry.toml](poetry.toml) it creates a virtual environment within the project repo. When e.g. running or testing the application, commands should be prefixed with `poetry run` as this runs the commands within the virtual environment. For example instead of running the application using `flask run`, use `poetry run flask run `. This will ensure the correct dependencies are available to the application.

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

## Testing the application

### Intro

The application is tested using [pytest](https://docs.pytest.org/en/stable/). Dependencies on pytest are managed via Poetry (like all other Python package dependencies), so you don't need to install pytest.

### Config

The end-to-end (E2E) tests use [Selenium](https://selenium-python.readthedocs.io/) to run. Selenium requires a browser-specific driver in order to run. These are listed [here](https://selenium-python.readthedocs.io/installation.html#drivers). This project is currently setup to use geckodriver, which is the the Firefox driver. Download the relevant version for you (listed [here](https://github.com/mozilla/geckodriver/releases)), unzip and place the executable either in the project repo root, or on your PATH. You'll also need to have Firefox installed.

### Running the tests

To run all tests, run `poetry run pytest`. You can also specify specific test folders, e.g.: `poetry run pytest tests_e2e`.

Adding the `-r` flag to the `pytest` command outputs some short test summary information. This flag takes multiple [options](https://docs.pytest.org/en/stable/usage.html#detailed-summary-report). It defaults to `-rfE` (info provided for failures and errors), but if you want info on all tests regardless of the result then you can use `-rA`.