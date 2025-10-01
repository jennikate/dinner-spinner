"""
Tests for the recipe & recipes endpoint resource in the `src.app.routes.v1/recipe_routes` module.
"""

# =====================================
#  Imports
# =====================================

import pytest

from src.app.schemas.recipes import RecipeResponseSchema

# =====================================
#  Body
# =====================================

@pytest.mark.usefixtures("seeded_recipes")
class TestDeleteRecipe:
    def test_delete_recipe(self, client, seeded_recipes):
        # Get a recipe and verify it exists
        recipe_id = str(seeded_recipes[0].id)
        original_response = client.get(f"/v1/recipes/{recipe_id}")
        data = original_response.get_json()

        expected_original_response = RecipeResponseSchema().dump(seeded_recipes[0])

        assert original_response.status_code == 200
        assert data == expected_original_response

        # delete the recipe
        delete_response = client.delete(f"/v1/recipes/{recipe_id}")
        assert delete_response.status_code == 200
        assert delete_response.get_json() == {"message": f"recipe id {recipe_id} deleted" }

        # verify recipe is no longer there
        new_get_response = client.get("/v1/recipes")
        assert original_response.get_json() not in new_get_response.get_json()
            