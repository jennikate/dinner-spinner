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

@pytest.mark.usefixtures("seeded_recipes_with_ingredients")
class TestPutRecipeWithIngredients:
    def test_put_recipe_all_fields_changed(self, client, seeded_recipes_with_ingredients):
        recipe_id = str(seeded_recipes_with_ingredients[0].id)

        updated_recipe = {
            "recipe_name": "My updated simple recipe",
            "instructions": [
                {"step_number": 1,"instruction": "New first instruction"},
                {"step_number": 2,"instruction": "New second instruction"}
            ],
            "notes": "Adding some notes",
            "ingredients": [
                {"ingredient_name": "SOY sauce"},
                {"ingredient_name": "Juniper Berries"}
            ]
        }

        expected_put_response = {
            'recipe_id': recipe_id, 
            'recipe_name': 'My updated simple recipe',
            'instructions': [
                {'instruction': 'New first instruction', 'step_number': 1}, 
                {'instruction': 'New second instruction', 'step_number': 2}
            ], 
            'notes': 'Adding some notes', 
            'recipe_ingredients': [
                {'amount': 1.0, 'ingredient_name': 'soy sauce'}, 
                {'amount': 1.0, 'ingredient_name': 'juniper berries'}
            ]
        }
        
        assert_recipe_update(
            client=client, 
            expected_response=expected_put_response, 
            recipe_id=recipe_id, 
            updated_recipe=updated_recipe, 
            expected_status = 200
        )
    

    def test_put_recipe_change_name(self, client, seeded_recipes_with_ingredients):
        recipe = seeded_recipes_with_ingredients[0]
        updated_recipe = {
            "recipe_name": "My updated simple recipe name",
            "instructions": recipe.instructions,
            "notes": recipe.notes
        }

        expected_put_response = {
            "recipe_id": str(recipe.id),
            "instructions": recipe.instructions,
            "notes": recipe.notes,
            "recipe_name": "My updated simple recipe name",
            'recipe_ingredients': [
                {'amount': 1.0, 'ingredient_name': 'milk'}, 
                {'amount': 1.0, 'ingredient_name': 'potato'}
            ]
        }

        assert_recipe_update(
            client=client, 
            expected_response=expected_put_response, 
            recipe_id=str(recipe.id), 
            updated_recipe=updated_recipe, 
            expected_status = 200
        )


    def test_put_recipe_change_note(self, client, seeded_recipes_with_ingredients):
        recipe = seeded_recipes_with_ingredients[0]

        updated_recipe = {
            "recipe_name": recipe.recipe_name,
            "instructions": recipe.instructions,
            "notes": "Adding a note now"
        }

        expected_put_response = {
            "recipe_id": str(recipe.id),
            "instructions": recipe.instructions,
            "notes": "Adding a note now",
            "recipe_name": recipe.recipe_name, 
            'recipe_ingredients': [
                {'amount': 1.0, 'ingredient_name': 'milk'}, 
                {'amount': 1.0, 'ingredient_name': 'potato'}
            ]
        }

        assert_recipe_update(
            client=client, 
            expected_response=expected_put_response, 
            recipe_id=str(recipe.id), 
            updated_recipe=updated_recipe, 
            expected_status = 200
        )

    
    def test_put_recipe_change_note_to_null(self, client, seeded_recipes_with_ingredients):
        recipe = seeded_recipes_with_ingredients[1] # has a notes field that is not none

        updated_recipe = {
            "recipe_name": recipe.recipe_name,
            "instructions": recipe.instructions,
            "notes": None
        }

        expected_put_response = {
            "recipe_id": str(recipe.id),
            "instructions": recipe.instructions,
            "notes": None,
            "recipe_name": recipe.recipe_name, 
            'recipe_ingredients': [
                {'amount': 1.0, 'ingredient_name': 'milk'}, 
                {'amount': 1.0, 'ingredient_name': 'potato'}
            ]
        }

        assert_recipe_update(
            client=client, 
            expected_response=expected_put_response, 
            recipe_id=str(recipe.id), 
            updated_recipe=updated_recipe, 
            expected_status = 200
        )

    
    def test_put_recipe_change_instruction(self, client, seeded_recipes_with_ingredients):
        recipe = seeded_recipes_with_ingredients[0]

        updated_recipe = {
            "recipe_name": recipe.recipe_name,
            "instructions": [
                {"step_number": 1,"instruction": "Step one do things"},
                {"step_number": 2,"instruction": "Step two do other things"}
            ],
            "notes": recipe.notes
        }

        expected_put_response = {
            **updated_recipe,
            "recipe_id": str(recipe.id), 
            'recipe_ingredients': [
                {'amount': 1.0, 'ingredient_name': 'milk'}, 
                {'amount': 1.0, 'ingredient_name': 'potato'}
            ]
        }

        assert_recipe_update(
            client=client, 
            expected_response=expected_put_response, 
            recipe_id=str(recipe.id), 
            updated_recipe=updated_recipe, 
            expected_status = 200
        )


    def test_put_recipe_change_ingredients(self, client, seeded_recipes_with_ingredients):
        recipe = seeded_recipes_with_ingredients[0]
        recipe_ingredient = recipe.recipe_ingredients[0]

        updated_recipe = {
            "recipe_name": recipe.recipe_name,
            "instructions": recipe.instructions,
            "notes": recipe.notes,
            "ingredients": [
                {"ingredient_name": "SOY sauce"},
                {"ingredient_name": "Juniper Berries"},
                {"ingredient_id": recipe_ingredient.id, "ingredient_name": recipe_ingredient.ingredient_name}
            ]
        }

        expected_put_response = {
            'recipe_id': str(recipe.id), 
            'recipe_name': recipe.recipe_name,
            'instructions': recipe.instructions, 
            'notes': recipe.notes,
            'recipe_ingredients': [
                {'amount': 1.0, 'ingredient_name': 'soy sauce'}, 
                {'amount': 1.0, 'ingredient_name': 'juniper berries'},
                {'amount': recipe_ingredient.amount, 'ingredient_name': recipe_ingredient.ingredient_name}
            ]
        }

        assert_recipe_update(
            client=client, 
            expected_response=expected_put_response, 
            recipe_id=str(recipe.id), 
            updated_recipe=updated_recipe, 
            expected_status = 200
        )


    def test_put_recipe_by_id_nothing_changed(self, client, seeded_recipes_with_ingredients):
        """
        Test that if nothing changes, we still return a 200
        """
        recipe = seeded_recipes_with_ingredients[0]
        updated_recipe = {
            "recipe_name": recipe.recipe_name,
            "instructions": recipe.instructions,
            "notes": recipe.notes
        }

        expected_response =  {
            "recipe_id": str(recipe.id), 
            "instructions": recipe.instructions, 
            "notes": recipe.notes,
            "recipe_name": recipe.recipe_name, 
            'recipe_ingredients': [
                {'amount': 1.0, 'ingredient_name': 'milk'}, 
                {'amount': 1.0, 'ingredient_name': 'potato'}
            ]
        }

        assert_recipe_update(
            client=client, 
            expected_response=expected_response, 
            recipe_id=str(recipe.id), 
            updated_recipe=updated_recipe, 
            expected_status = 200
        ) 
