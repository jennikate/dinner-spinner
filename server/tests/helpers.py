"""
Common functions used in tests.
"""
# =====================================
# Imports
# =====================================

from sqlalchemy.exc import SQLAlchemyError

from src.app.extensions import db as _db

# =====================================
# Body
# =====================================

# --------------------
# ENDPOINT
# --------------------

def call_endpoint(client, endpoint, method, payload):
    # Dynamically get the method from the client (post, get, patch, etc.)
    func = getattr(client, method.lower())

    # Decide whether to send payload or not
    if method.lower() in ["post", "patch", "put"]:
        return func(endpoint, json=payload)
    else:
        return func(endpoint)

# --------------------
# DB ERRORS
# --------------------

def assert_sqlalchemy_error(client, monkeypatch, endpoint, method, payload):
        """
        Asserts a 500 response with a message is returned if an SQLAlchemy error is raised
        """
        # Monkeypatch db.session.commit to raise SQLAlchemyError
        def bad_commit():
            raise SQLAlchemyError("DB error")

        monkeypatch.setattr(_db.session, "commit", bad_commit)
        response = call_endpoint( client=client, endpoint=endpoint, method=method, payload=payload)

        assert response.status_code == 500
        data = response.get_json()
        assert "An error occurred writing to the db" in data["message"]

def assert_generic_error(client, monkeypatch, endpoint, method, payload):
        """
        Tests that a 500 response with a message if a GenericError is raised
        """
        def bad_commit():
            raise RuntimeError("Something went wrong!")

        monkeypatch.setattr(_db.session, "commit", bad_commit)
        response = call_endpoint( client=client, endpoint=endpoint, method=method, payload=payload)
        
        assert response.status_code == 500
        data = response.get_json()
        assert "An error occurred writing to the db" in data["message"] 
