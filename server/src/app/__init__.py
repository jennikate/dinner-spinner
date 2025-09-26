"""
Providing the create_app() function that applies config and 
returns the Flask application instance.
"""
# =====================================
# Imports
# =====================================

import logging
import os

from flask import Flask

from .config import config
from .extensions import api, db, migrate
from .routes.v1.recipe_routes import blp as RecipeBlueprint
from .models import * # Import models so they are registered with SQLAlchemy


# =====================================
# Body
# =====================================
def register_blueprints(app):
    app.logger.debug("---------- Starting register_blueprints ----------")
    
    app.register_blueprint(RecipeBlueprint)

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
    register_extensions(app)
    register_blueprints(app)

    app.logger.debug(f"Database location -> {config[config_name].SQLALCHEMY_DATABASE_URI}")
    app.logger.info("---------- Finished create_app ----------")
    return app