"""
Tests for the recipe & recipes endpoint resource in the `src.app.routes.v1/recipe_routes` module.
"""

# =====================================
#  Imports
# =====================================

import pytest

from src.app.extensions import db as _db
from ....helpers import assert_generic_error, assert_sqlalchemy_error

# =====================================
#  Body
# =====================================

@pytest.mark.usefixtures("seeded_recipes")
class TestDeleteRecipeWithDbErrors:
    def test_delete_recipe_sqlalchemy_error(self, client, monkeypatch, seeded_recipes):
        """
        Tests a 500 response with a message is returned if an SQLAlchemy error is raised
        """
        recipe_id = str(seeded_recipes[0].id)
        # Call the reusable helper
        assert_sqlalchemy_error(
            client=client,
            monkeypatch=monkeypatch,
            method="delete",
            endpoint=f"/v1/recipes/{recipe_id}"
        )

    
    def test_post_recipe_generic_error(self, client, monkeypatch, seeded_recipes):
        """
        Tests that a 500 response with a message if a GenericError is raised
        """
        recipe_id = str(seeded_recipes[0].id)
        assert_generic_error(
            client=client,
            monkeypatch=monkeypatch,
            method="delete",
            endpoint=f"/v1/recipes/{recipe_id}"
        )
