"""
Tests for adding an ingredient.
"""

# =====================================
#  Imports
# =====================================

import pytest

from uuid import UUID

from src.app.schemas.ingredients import IngredientResponseSchema
from src.app.routes.v1.ingredient_routes import add_ingredients

# =====================================
#  Body
# =====================================

class TestAddIngredientStaticMethod:
    def test_add_new_ingredient(self):
        """
        Tests the static method adds ingredients to the db
        """
        ingredients = [
            {
                "ingredient_name": "Milk"
            }, 
            {
                "ingredient_name": "Eggs"
            }
        ]

        result = add_ingredients(ingredients)
        names = [r.ingredient_name for r in result]

        assert names == ["Milk", "Eggs"]


@pytest.mark.usefixtures("seeded_ingredients")
class TestAddIngredientStaticMethodWithExisting:   
    def test_add_existing_ingredient(self, seeded_ingredients):
        """
        Tests the static method doesn't readd an existing ingredient when ID provided
        """
        # Get an ingredient
        schema = IngredientResponseSchema() # make instance of the class
        seeded = schema.dump(seeded_ingredients[0])

        ingredients = [
            {
                "id": UUID(seeded["ingredient_id"]), # add_ingredients can take an 'id' as a UUID
                "ingredient_name": seeded["ingredient_name"]
            },
            {
                "ingredient_name": "Milk"
            }, 
            {
                "ingredient_name": "Eggs"
            }
        ]

        result = add_ingredients(ingredients)

        # check we didn't create a NEW version of the existing ingredient
        for item in result:
            if item.ingredient_name == seeded["ingredient_name"]:
                assert item.id == UUID(seeded["ingredient_id"])

        # check it returns ALL ingredients
        names = [r.ingredient_name for r in result]
        assert names == [
            seeded["ingredient_name"],
            "Milk",
            "Eggs"
        ]
