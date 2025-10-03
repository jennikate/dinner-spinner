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
# UPDATES
# --------------------

def assert_recipe_update(client, expected_response, recipe_id, updated_recipe, expected_status = 200):
    """
    Reusable helper to assert that updating a recipe works as expected.
    """
    print(f"updated_recipe -> {updated_recipe}")
    # Get the original recipe
    original_response = client.get(f"/v1/recipes/{recipe_id}")
    original_data = original_response.get_json()

    # Verify that the update actually changes something
    assert original_data != updated_recipe

    # Perform the update
    update_response = client.put(f"/v1/recipes/{recipe_id}", json=updated_recipe)
    print(f"update_response -> {update_response.get_json()}")

    # Assert put code and response
    assert update_response.status_code == expected_status
    assert update_response.get_json() == expected_response

    # get recipe from db
    updated_response = client.get(f"/v1/recipes/{recipe_id}")
    updated_data = updated_response.get_json()

    assert updated_data == expected_response


# --------------------
# ENDPOINT
# --------------------

def call_endpoint(client, endpoint, method, payload):
    # Dynamically get the method from the client (post, get, put, etc.)
    func = getattr(client, method.lower())

    # Decide whether to send payload or not
    if method.lower() in ["post", "put", "put"]:
        return func(endpoint, json=payload)
    else:
        return func(endpoint)

# --------------------
# DB ERRORS
# --------------------

def assert_sqlalchemy_error(*, client, monkeypatch, endpoint, method, payload=None):
        # * makes all following args mandatory UNLESS you include =None
        # so here only payload is optional
        """
        Asserts a 500 response with a message is returned if an SQLAlchemy error is raised
        """
        # Monkeypatch db.session.commit to raise SQLAlchemyError
        def bad_commit():
            raise SQLAlchemyError("DB error")
        
        print(f"payload -> {payload}")
        print(f"method -> {method}")

        monkeypatch.setattr(_db.session, "commit", bad_commit)
        response = call_endpoint(client=client, endpoint=endpoint, method=method, payload=payload)

        assert response.status_code == 500
        data = response.get_json()
        assert "An error occurred writing to the db" in data["message"]

def assert_generic_error(*, client, monkeypatch, endpoint, method, payload=None):
        """
        Tests that a 500 response with a message if a GenericError is raised
        """
        def bad_commit():
            raise RuntimeError("Something went wrong!")

        monkeypatch.setattr(_db.session, "commit", bad_commit)
        response = call_endpoint(client=client, endpoint=endpoint, method=method, payload=payload)
        
        assert response.status_code == 500
        data = response.get_json()
        assert "An error occurred writing to the db" in data["message"] 
