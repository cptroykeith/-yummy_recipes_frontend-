""" This file has initialization code for the app """

from flask import Flask

# get the configurations
from configuration.config import APP_CONFIG


def create_app(config_name):
    """
    This is a wrapper for creation of the flask app
    based on the environment
    """
    app = Flask(__name__)
    app.config.from_object(APP_CONFIG[config_name])

    return app
