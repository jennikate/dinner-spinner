"""
Main entry point for the Flask application. This script creates the Flask application instance using
create_app().

create_app is in src/__init__.py and does the app config & blueprint registration
"""
# =====================================
# Imports
# =====================================

import logging
import os

from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

from .app import create_app

# =====================================
# Body
# =====================================

# load variables from .env file into os.environ and overwrite any existing environment variables
load_dotenv(override=True)

# ---------------------------
# CREATE APP
# ---------------------------
# Get the config to load (dev, test, prod) from the env var to call the relevant config
# If no env var exists do NOT default, throw error forcing user to set the config they want
config_level = os.getenv("FLASK_ENV", None)
if config_level is None:
    print('===== ERROR: You have not specified a config level')

app = create_app(config_level)


# ---------------------------
# SETUP LOGGER
# ---------------------------
log_level = os.getenv("LOG_LEVEL", "INFO") # default to info
# Remove default handler
del app.logger.handlers[:]

if app.debug:
    log_handler = logging.StreamHandler()
else:
    log_handler = RotatingFileHandler("flask_api_log.log", maxBytes=10000, backupCount=1)

log_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
app.logger.setLevel(log_level) # levels used: DEBUG, INFO, WARNING, ERROR, CRITICAL
app.logger.addHandler(log_handler)


# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    # Accept "1"/"0" or "true"/"false" (case-insensitive)
    debug_env = os.getenv("FLASK_DEBUG", "0").lower()
    debug_mode = debug_env in ("1", "true", "yes")

    app.logger.debug("---------- Starting App ----------")
    app.logger.info(f"Running with config for: {config_level}")
    app.logger.info(f"Running in debug mode? {debug_mode}")
    app.logger.info(f"Log level: {log_level}")

    app.run(debug=debug_mode, host="0.0.0.0")
