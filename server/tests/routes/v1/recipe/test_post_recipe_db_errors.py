"""
Tests for the recipe & recipes endpoint resource in the `src.app.routes.v1/recipe_routes` module.
"""

# =====================================
#  Imports
# =====================================

from src.app.extensions import db as _db
from ....fixtures import base_recipe
from ....helpers import assert_generic_error, assert_sqlalchemy_error

# =====================================
#  Body
# =====================================

class TestPostRecipeWithDbErrors:
    def test_post_recipe_sqlalchemy_error(self, client, monkeypatch, base_recipe):
        """
        Tests a 500 response with a message is returned if an SQLAlchemy error is raised
        """
        # Call the reusable helper
        assert_sqlalchemy_error(
            client=client,
            monkeypatch=monkeypatch,
            method="post",
            endpoint="/v1/recipes",
            payload=base_recipe
        )

    
    def test_post_recipe_generic_error(self, client, monkeypatch, base_recipe):
        """
        Tests that a 500 response with a message if a GenericError is raised
        """
        assert_generic_error(
            client=client,
            monkeypatch=monkeypatch,
            method="post",
            endpoint="/v1/recipes",
            payload=base_recipe
        )


