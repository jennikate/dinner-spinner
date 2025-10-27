"""
Tests for the recipe & recipes endpoint resource in the `src.app.routes.v1/recipe_routes` module.
"""

# =====================================
#  Imports
# =====================================

from ....fixtures import base_recipe, base_recipe_with_ingredients, base_recipe_with_ingredients_response

# =====================================
#  Body
# =====================================

class TestPostRecipe:
    def test_post_recipe_mandatory_only(self, client, base_recipe):
        """
        Tests only the required fields are sent.
        """
        response = client.post("/v1/recipes", json=base_recipe)
        data = response.get_json()

        expected_response = {
            **base_recipe, # unpack (spread operator)
            "recipe_id": data["recipe_id"], # UUID is generated
            "notes": None,
            "recipe_ingredients": []
        }

        assert response.status_code == 201
        assert data == expected_response


    def test_post_recipe_with_new_ingredients(self, client, base_recipe_with_ingredients, base_recipe_with_ingredients_response):
        """
        Tests only the required fields are sent.
        """
        response = client.post("/v1/recipes", json=base_recipe_with_ingredients)
        data = response.get_json()

        expected_response = {
            **base_recipe_with_ingredients_response, # unpack (spread operator)
            "recipe_id": data["recipe_id"], # UUID is generated
            "notes": None
        }

        assert response.status_code == 201
        assert data == expected_response


    def test_post_recipe_with_notes(self, client, base_recipe):
        """
        Tests all fields are sent.
        """
        new_recipe = {
            **base_recipe,
            "notes": "I wrote some notes"
        }

        response = client.post("/v1/recipes", json=new_recipe)
        data = response.get_json()

        expected_response = {
            **base_recipe, # unpack (spread operator)
            "recipe_id": data["recipe_id"], # UUID is generated
            "notes": "I wrote some notes",
            "recipe_ingredients": []
        }

        assert response.status_code == 201
        assert data == expected_response


    def test_post_recipe_string_steps_are_converted_to_int(self, client, base_recipe):
        """
        Tests even if we send the step as a string its accepted and returned.
        """
        new_recipe = {
            "recipe_name": "My simple recipe",
            "instructions": [
                {
                    "step_number": "1",
                    "instruction": "First thing you do is"
                },
                {
                    "step_number": 2,
                    "instruction": "Second thing you do is"
                }
            ]
        } 
        response = client.post("/v1/recipes", json=new_recipe)
        data = response.get_json()

        expected_response = {
            **base_recipe, # unpack (spread operator)
            "recipe_id": data["recipe_id"], # UUID is generated
            "notes": None,
            "recipe_ingredients": []
        }

        assert response.status_code == 201
        assert data == expected_response

