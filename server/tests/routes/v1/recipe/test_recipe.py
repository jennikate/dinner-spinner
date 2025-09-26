"""
Tests for the recipe & recipes endpoint resource in the `src.app.routes.v1/recipe_routes` module.
"""

# =====================================
#  Imports
# =====================================


# =====================================
#  Body
# =====================================

class TestPostRecipe:
    def test_post_recipe_name_only(self, client):
        """
        Tests the bare minimum for recipe creation can be posted - a name.
        """
        new_recipe = {
            "recipe_name": "My simple recipe",
            "instructions": [
                {
                "step_number": 1,
                "instruction": "First thing you do is"
                },
                {
                "step_number": 2,
                "instruction": "Second thing you do is"
                }
            ]
        }

        response = client.post("/v1/recipe", json=new_recipe)
        data = response.get_json()

        expected_response = {
            "id": data["id"], # UUID is generated
            "recipe_name": "My simple recipe",
            "instructions": [
                {
                "step_number": 1,
                "instruction": "First thing you do is"
                },
                {
                "step_number": 2,
                "instruction": "Second thing you do is"
                }
            ]
        }

        assert response.status_code == 201
        assert data == expected_response


