"""
Tests for the recipe & recipes endpoint resource in the `src.app.routes.v1/recipe_routes` module.
"""

# =====================================
#  Imports
# =====================================

import json
import pytest

from src.app.schemas.recipes import RecipeResponseSchema
from ....helpers import assert_recipe_update

# =====================================
#  Body
# =====================================

@pytest.mark.usefixtures("seeded_recipes")
class TestPutRecipe:
    def test_put_recipe_all_fields_changed(self, client, seeded_recipes):
        recipe_id = str(seeded_recipes[0].id)

        updated_recipe = {
            "recipe_name": "My updated simple recipe",
            "instructions": [
                {"step_number": 1,"instruction": "New first instruction"},
                {"step_number": 2,"instruction": "New second instruction"}
            ],
            "notes": "Adding some notes"
        }

        expected_put_response = {
            "id": recipe_id,
            "instructions": [
                {"step_number": 1,"instruction": "New first instruction"},
                {"step_number": 2,"instruction": "New second instruction"}
            ],
            "notes": "Adding some notes",
            "recipe_name": "My updated simple recipe"
        }

        assert_recipe_update(
            client=client, 
            expected_response=expected_put_response, 
            recipe_id=recipe_id, 
            updated_recipe=updated_recipe, 
            expected_status = 200
        )
    

    def test_put_recipe_change_name(self, client, seeded_recipes):
        recipe = seeded_recipes[0]
        instructions_list = json.loads(recipe.instructions)

        updated_recipe = {
            "recipe_name": "My updated simple recipe name",
            "instructions": instructions_list,
            "notes": recipe.notes
        }

        expected_put_response = {
            "id": str(recipe.id),
            "instructions": instructions_list,
            "notes": recipe.notes,
            "recipe_name": "My updated simple recipe name"
        }

        assert_recipe_update(
            client=client, 
            expected_response=expected_put_response, 
            recipe_id=str(recipe.id), 
            updated_recipe=updated_recipe, 
            expected_status = 200
        )


    def test_put_recipe_change_note(self, client, seeded_recipes):
        recipe = seeded_recipes[0]
        instructions_list = json.loads(recipe.instructions)

        updated_recipe = {
            "recipe_name": recipe.name,
            "instructions": instructions_list,
            "notes": "Adding a note now"
        }

        expected_put_response = {
            "id": str(recipe.id),
            "instructions": instructions_list,
            "notes": "Adding a note now",
            "recipe_name": recipe.name
        }

        assert_recipe_update(
            client=client, 
            expected_response=expected_put_response, 
            recipe_id=str(recipe.id), 
            updated_recipe=updated_recipe, 
            expected_status = 200
        )

    
    def test_put_recipe_change_instruction(self, client, seeded_recipes):
        recipe = seeded_recipes[0]

        updated_recipe = {
            "recipe_name": recipe.name,
            "instructions": [
                {"step_number": 1,"instruction": "Step one do things"},
                {"step_number": 2,"instruction": "Step two do other things"}
            ],
            "notes": recipe.notes
        }

        expected_put_response = {
            **updated_recipe,
            "id": str(recipe.id)
        }

        assert_recipe_update(
            client=client, 
            expected_response=expected_put_response, 
            recipe_id=str(recipe.id), 
            updated_recipe=updated_recipe, 
            expected_status = 200
        )
