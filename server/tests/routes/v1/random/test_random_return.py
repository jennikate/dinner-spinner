"""
Tests for randomly returning recipes.
"""

# =====================================
#  Imports
# =====================================

import pytest

from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

from src.app.constants import DEFAULT_RANDOM_RECIPES
from src.app.extensions import db as _db
from src.app.services.ingredient_services import IngredientService

from tests.helpers import serialize_ingredients


# =====================================
#  Body
# =====================================

@pytest.mark.usefixtures("large_seeded_recipes")
class TestReturnRandomRecipes:
    def test_return_default_amount(self, client):
        """
        Tests the default amount from constants is used
        """
        response = client.post("/v1/random")
        data = response.get_json()

        assert response.status_code == 200
        assert len(data) == DEFAULT_RANDOM_RECIPES

        # Check each id returned is unique
        ids = [item["recipe_id"] for item in data]
        assert len(ids) == len(set(ids)), "Duplicate IDs returned in random selection"
        
        # Check that each recipe only has the expected keys
        expected_keys = {"recipe_id", "recipe_name"}

        for item in data:
            assert set(item.keys()) == expected_keys, f"Unexpected keys in item: {item.keys()}"
            assert all(item[k] for k in expected_keys), "Missing or empty field in recipe"


    def test_return_random(self, client):
        """
        Best effort to test a random list is returned
        """
        data1 = client.post("/v1/random").get_json()
        data2 = client.post("/v1/random").get_json()

        ids1 = {item["recipe_id"] for item in data1}
        ids2 = {item["recipe_id"] for item in data2}
        
        # The sets should not always be identical
        assert ids1 != ids2, "Both calls returned same results"


    def test_return_with_pinned(self, client, large_seeded_recipes):
        """
        Tests the default amount from constants is used
        """
        data_to_post = {
            "pin": [
                large_seeded_recipes[5].id,
                large_seeded_recipes[30].id
            ]
        }
        response = client.post("/v1/random", json=data_to_post)
        data = response.get_json()

        assert response.status_code == 200
        assert len(data) == DEFAULT_RANDOM_RECIPES

        # Check the pinned ID is in the results
        ids = [item["recipe_id"] for item in data]
        assert str(large_seeded_recipes[5].id) in ids
        assert str(large_seeded_recipes[30].id) in ids
        
        
    def test_return_requested_amount(self, client):
        """
        Tests the default amount from constants is used
        """
        data_to_post = {
            "number": 3,
        }
        response = client.post("/v1/random", json=data_to_post)
        data = response.get_json()

        assert response.status_code == 200
        assert len(data) == 3
            
            
    def test_return_requested_amount_and_pinned(self, client, large_seeded_recipes):
        """
        Tests the default amount from constants is used
        """
        data_to_post = {
            "number": 7,
            "pin": [
                large_seeded_recipes[35].id,
                large_seeded_recipes[21].id
            ]
        }
        response = client.post("/v1/random", json=data_to_post)
        data = response.get_json()

        assert response.status_code == 200
        assert len(data) == 7
        
        # Check the pinned ID is in the results
        ids = [item["recipe_id"] for item in data]
        assert str(large_seeded_recipes[35].id) in ids
        assert str(large_seeded_recipes[21].id) in ids


@pytest.mark.usefixtures("seeded_recipes_with_ingredients")
class TestReturnRandomRecipesNotEnough:
    def test_return_when_not_enough_to_meet_default(self, client, seeded_recipes_with_ingredients):
        """
        Tests the default amount from constants is used
        """
        response = client.post("/v1/random")
        data = response.get_json()

        assert response.status_code == 200
        assert len(data) == len(seeded_recipes_with_ingredients)
        



