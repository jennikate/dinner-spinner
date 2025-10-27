"""
Common fixtures for tests.
"""
# =====================================
# Imports
# =====================================

import pytest

# =====================================
# Body
# =====================================

@pytest.fixture
def base_recipe():
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
    return new_recipe

@pytest.fixture
def base_recipe_with_ingredients():
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
        ],
        "ingredients": [
            {
                "ingredient_name": "milk"
            },
            {
                "ingredient_name": "sugar"
            }
        ]
    } 
    return new_recipe

@pytest.fixture
def base_recipe_with_ingredients_response():
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
        ],
        "recipe_ingredients": [
            {
                "amount": 1.0,
                "ingredient_name": "milk"
            },
            {
                "amount": 1.0,
                "ingredient_name": "sugar"
            }
        ]
    } 
    return new_recipe
