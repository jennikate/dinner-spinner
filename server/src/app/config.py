"""
Application configuration.
"""
# =====================================
# Imports
# =====================================

import os
import secrets

# =====================================
# Body
# =====================================

class BaseConfig:
    """
    BaseConfig configuration settings for all environments.
    """

    # ---------------------------
    # FLASK CONFIG
    # ---------------------------
    # if an exception occurs hidden inside an extension of Flask, propogate it into the main app so we can see it
    PROPAGATE_EXCEPTIONS = True


    # ---------------------------
    # SMOREST CONFIG
    # ---------------------------
    API_TITLE = "Dinner Spinner REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # ---------------------------
    # SQLALCHEMY CONFIG
    # ---------------------------
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'database.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)


class ProductionConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")


config = {
    "DEV": DevelopmentConfig,
    "TEST": TestingConfig,
    "PROD": ProductionConfig,
}
