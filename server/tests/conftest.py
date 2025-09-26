"""
Config for tests.
"""

###################################################################################################
# Imports
###################################################################################################

import os
import pytest

from alembic import command
from alembic.config import Config
from sqlalchemy.orm import sessionmaker, scoped_session

from src.app import create_app, db as _db # _db to be clear this is the test instance

###################################################################################################
# Configuration & setup
###################################################################################################

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MIGRATIONS_DIR = os.path.join(BASE_DIR, "migrations")

@pytest.fixture
def db():
    """Expose the SQLAlchemy db object for tests."""
    return _db


@pytest.fixture(scope="session")
def app():
    """Create Flask app in testing config and push context."""
    app = create_app("TEST")
    with app.app_context():
        yield app  # app context is active for the duration of the session

@pytest.fixture
def client(app):
    return app.test_client()

# NOTES:
# scope="session": runs once per test session, not per test function.
# autouse=True: automatically applies to all tests — you don’t have to pass it as a parameter.
@pytest.fixture(scope="session", autouse=True)
def apply_migrations(app):
    db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
    
    # Remove the file if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Apply migrations with Alembic
    alembic_cfg = Config(os.path.join(MIGRATIONS_DIR, "alembic.ini"))
    alembic_cfg.set_main_option("script_location", MIGRATIONS_DIR)
    alembic_cfg.set_main_option("sqlalchemy.url", app.config["SQLALCHEMY_DATABASE_URI"])
    command.upgrade(alembic_cfg, "head")
    
    yield
    
    # optional: cleanup
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture(scope="function", autouse=True)
def session(app):
    """Run each test in its own transaction (rollback after)."""
    connection = _db.engine.connect()
    transaction = connection.begin()

    SessionFactory = sessionmaker(bind=connection, expire_on_commit=False)
    session = scoped_session(SessionFactory)

    _db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()
