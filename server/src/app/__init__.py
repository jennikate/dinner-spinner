"""
Providing the create_app() function that applies config and 
returns the Flask application instance.
"""
###################################################################################################
# Imports
###################################################################################################

import logging
import os

from flask import Flask

from app.config import config
from app.extensions import api, db, migrate
import app.models


###################################################################################################
# Body
###################################################################################################
def register_blueprints(app):
    app.logger.debug("---------- Starting register_blueprints ----------")
    
    app.logger.debug("---------- Finished register_blueprints ----------")


def register_extensions(app):
    app.logger.debug("---------- Starting register_extensions ----------")
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    app.logger.debug("---------- Finished register_extensions ----------")


def create_app(config_name):
    """
    Create a Flask application using the app factory pattern. Registers extensions and blueprints using
    local functions.
    """
    app = Flask(__name__)
    app.logger.info("---------- Starting create_app ----------")
    app.config.from_object(config[config_name])
    app.logger.debug(f"CONFIG -> {config[config_name].SQLALCHEMY_DATABASE_URI}")
    register_extensions(app)
    register_blueprints(app)

    db_path = config[config_name].SQLALCHEMY_DATABASE_URI.replace("sqlite:///", "")
    print("Absolute path:", os.path.abspath(db_path))
    app.logger.info("---------- Finished create_app ----------")
    return app