"""
Tests for adding an ingredient.
"""

# =====================================
#  Imports
# =====================================

import pytest

from uuid import UUID

from src.app.schemas.ingredients import IngredientResponseSchema
from src.app.services.ingredient_services import IngredientService
from tests.helpers import serialize_ingredients

# =====================================
#  Body
# =====================================

class TestAddIngredientStaticMethod:
    def test_add_new_ingredient(self):
        """
        Tests the static method adds ingredients to the db
        """
        ingredients = [
            { "ingredient_name": "Milk" }, 
            { "ingredient_name": "Eggs" }
        ]

        response = IngredientService.save_ingredients(ingredients)

        expected_response = {
            "failed": [], 
            "saved": [
                { "ingredient_name": "milk" },
                { "ingredient_name": "eggs" }
            ]    
        }

        assert {
            "saved": serialize_ingredients(response["saved"]),
            "failed": serialize_ingredients(response["failed"])
        } == expected_response

    
    def test_add_new_ingredient_with_invalid_id(self):
        """
        Tests the static method adds ingredients to the db
        """
        ingredients = [
            { "id": UUID("11111111-6ce2-48ca-a262-04036209b03c"), "ingredient_name": "Milk" }, 
            { "ingredient_name": "Eggs" }
        ]

        response = IngredientService.save_ingredients(ingredients)

        expected_response = {
            "failed": [], 
            "saved": [
                { "ingredient_name": "milk" },
                { "ingredient_name": "eggs" }
            ]    
        }

        assert {
            "saved": serialize_ingredients(response["saved"]),
            "failed": serialize_ingredients(response["failed"])
        } == expected_response


@pytest.mark.usefixtures("seeded_ingredients")
class TestAddIngredientStaticMethodWithExisting:   
    def test_add_existing_ingredient_by_id(self, seeded_ingredients):
        """
        Tests the static method doesn't readd an existing ingredient when ID provided
        """
        # Get an ingredient
        schema = IngredientResponseSchema() # make instance of the class
        seeded = schema.dump(seeded_ingredients[0])

        ingredients = [
            {
                "id": UUID(seeded["ingredient_id"]), # save_ingredients can take an 'id' as a UUID
                "ingredient_name": seeded["ingredient_name"]
            },
            {
                "ingredient_name": "Milk"
            }, 
            {
                "ingredient_name": "Eggs"
            }
        ]

        response = IngredientService.save_ingredients(ingredients)

        # check we didn't create a NEW version of the existing ingredient
        for item in response["saved"]:
            if item.ingredient_name == seeded["ingredient_name"]:
                assert item.id == UUID(seeded["ingredient_id"])

        expected_response = {
            "failed": [], 
            "saved": [
                { "ingredient_name": seeded["ingredient_name"] },
                { "ingredient_name": "milk" },
                { "ingredient_name": "eggs" }
            ]    
        }

        assert {
            "saved": serialize_ingredients(response["saved"]),
            "failed": serialize_ingredients(response["failed"])
        } == expected_response


    def test_add_existing_ingredient_by_string(self, seeded_ingredients):
        """
        Tests the static method doesn't readd an existing ingredient when ID provided
        """
        # Get an ingredient
        schema = IngredientResponseSchema() # make instance of the class
        seeded = schema.dump(seeded_ingredients[0])

        ingredients = [
            {
               "ingredient_name": seeded["ingredient_name"]
            },
            {
                "ingredient_name": "Milk"
            }, 
            {
                "ingredient_name": "Eggs"
            }
        ]

        response = IngredientService.save_ingredients(ingredients)

        # check we didn't create a NEW version of the existing ingredient
        for item in response["saved"]:
            if item.ingredient_name == seeded["ingredient_name"]:
                assert item.id == UUID(seeded["ingredient_id"])

        expected_response = {
            "failed": [], 
            "saved": [
                { "ingredient_name": seeded["ingredient_name"].lower() },
                { "ingredient_name": "milk" },
                { "ingredient_name": "eggs" }
            ]    
        }

        assert {
            "saved": serialize_ingredients(response["saved"]),
            "failed": serialize_ingredients(response["failed"])
        } == expected_response
