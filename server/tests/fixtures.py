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

