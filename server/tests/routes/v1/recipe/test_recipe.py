"""
Tests for the recipe & recipes endpoint resource in the `src.app.routes.v1/recipe_routes` module.
"""

# =====================================
#  Imports
# =====================================

from ....fixtures import base_recipe

# =====================================
#  Body
# =====================================

class TestPostRecipe:
    def test_post_recipe_name_only(self, client, base_recipe):
        """
        Tests the bare minimum for recipe creation can be posted - a name.
        """
        response = client.post("/v1/recipe", json=base_recipe)
        data = response.get_json()

        expected_response = {
            **base_recipe, # unpack (spread operator)
            "id": data["id"], # UUID is generated
            "notes": None
        }

        assert response.status_code == 201
        assert data == expected_response


    def test_post_recipe_with_notes(self, client, base_recipe):
        """
        Tests the bare minimum for recipe creation can be posted - a name.
        """
        new_recipe = {
            **base_recipe,
            "notes": "I wrote some notes"
        }

        response = client.post("/v1/recipe", json=new_recipe)
        data = response.get_json()

        expected_response = {
            **base_recipe, # unpack (spread operator)
            "id": data["id"], # UUID is generated
            "notes": "I wrote some notes"
        }

        assert response.status_code == 201
        assert data == expected_response


