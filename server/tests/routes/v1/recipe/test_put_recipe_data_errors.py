"""
Tests for the recipe & recipes endpoint resource in the `src.app.routes.v1/recipe_routes` module.
"""

# =====================================
#  Imports
# =====================================

import pytest

from ....helpers import assert_recipe_update

# =====================================
#  Body
# =====================================

@pytest.mark.usefixtures("seeded_recipes")
class TestPutRecipe:
    def test_put_recipe_by_id_invalid_id(self, client, seeded_recipes):
        # It needs a valid payload as that is checked before we check the uuid exists
        recipe = seeded_recipes[0]
        updated_recipe = {
            "recipe_name": recipe.recipe_name,
            "instructions": recipe.instructions,
            "notes": "Changing the note so something is updating"
        }

        expected_response =  {
            "code": 400,
            "message": "Invalid recipe id",
            "status": "Bad Request"
        }

        assert_recipe_update(
            client=client, 
            expected_response=expected_response, 
            recipe_id='abc123-format-of-uuid-invalid', 
            updated_recipe=updated_recipe, 
            expected_status = 400
        )
        

    def test_put_recipe_by_id_bad_uuid(self, client, seeded_recipes):
        recipe = seeded_recipes[0]
        updated_recipe = {
            "recipe_name": "Changing name so something tries to update",
            "instructions": recipe.instructions,
            "notes": recipe.notes
        }

        expected_response =  {
            "code": 400,
            "message": "Invalid recipe id",
            "status": "Bad Request"
        }

        assert_recipe_update(
            client=client, 
            expected_response=expected_response, 
            recipe_id='bad_id', 
            updated_recipe=updated_recipe, 
            expected_status = 400
        )


    def test_put_recipe_by_id_uuid_doesnt_exist(self, client, seeded_recipes):
        recipe = seeded_recipes[0]
        updated_recipe = {
            "recipe_name": "New name so something tries to update",
            "instructions": recipe.instructions,
            "notes": recipe.notes
        }

        expected_response =  {
            "code": 404,
            "message": "Recipe not found",
            "status": "Not Found"
        }

        assert_recipe_update(
            client=client, 
            expected_response=expected_response, 
            recipe_id='21d634fd-e75f-49a0-85be-0e6815a1daf0', # random uuid
            updated_recipe=updated_recipe, 
            expected_status = 404
        )


    def test_put_recipe_by_id_invalid_id(self, client, seeded_recipes):
        # It needs a valid payload as that is checked before we check the uuid exists
        recipe = seeded_recipes[0]
        updated_recipe = {
            "recipe_name": recipe.recipe_name,
            "instructions": recipe.instructions,
            "notes": "Changing the note so something is updating"
        }

        expected_response =  {
            "code": 400,
            "message": "Invalid recipe id",
            "status": "Bad Request"
        }

        assert_recipe_update(
            client=client, 
            expected_response=expected_response, 
            recipe_id='abc123-format-of-uuid-invalid', 
            updated_recipe=updated_recipe, 
            expected_status = 400
        )
        
    
    def test_put_recipe_by_id_invalid_data(self, client, seeded_recipes):
        # It needs a valid payload as that is checked before we check the uuid exists
        recipe = seeded_recipes[0]
        updated_recipe = {
            "recipe_name": 123,
            "instructions": 'bob',
            "notes": 123
        }

        expected_response =  {
            "code": 422,
            "errors": {
                "json": {
                    "instructions": [
                        "Not a valid list."
                    ],
                    "notes": [
                        "Not a valid string."
                    ],
                    "recipe_name": [
                        "Not a valid string."
                    ]
                }
            },
            "status": "Unprocessable Entity"
        }

        assert_recipe_update(
            client=client, 
            expected_response=expected_response, 
            recipe_id='abc123-format-of-uuid-invalid', 
            updated_recipe=updated_recipe, 
            expected_status = 422
        )
    
    
    def test_put_recipe_by_id_invalid_instruction_data(self, client, seeded_recipes):
        # It needs a valid payload as that is checked before we check the uuid exists
        recipe = seeded_recipes[0]
        updated_recipe = {
            "recipe_name": recipe.recipe_name,
            "instructions": [
                {
                    "instruction": 1,
                    "step_number": "first instruction"
                },
                {
                    "step_number": "bob"
                },
                {
                    "step_number": True
                }
            ],
            "notes": recipe.notes
        }


        expected_response =  {
            "code": 422,
            "errors": {
                "json": {
                    "instructions": {
                        "0": {
                            "instruction": [
                                "Not a valid string."
                            ],
                            "step_number": [
                                "Not a valid integer."
                            ]
                        },
                        "1": {
                            "instruction": [
                                "Missing data for required field."
                            ],
                            "step_number": [
                                "Not a valid integer."
                            ]
                        },
                        "2": {
                            "instruction": [
                                "Missing data for required field."
                            ],
                            "step_number": [
                                "Not a valid integer."
                            ]
                        }
                    }
                }
            },
            "status": "Unprocessable Entity"
        }

        assert_recipe_update(
            client=client, 
            expected_response=expected_response, 
            recipe_id=str(recipe.id), 
            updated_recipe=updated_recipe, 
            expected_status = 422
        )


    def test_put_recipe_by_id_missing_mandatory_fields(self, client, seeded_recipes):
        # It needs a valid payload as that is checked before we check the uuid exists
        recipe = seeded_recipes[0]
        updated_recipe = {
            "notes": "new note"
        }

        expected_response =  {
            "code": 422,
            "errors": {
                "json": {
                    "instructions": [
                        "Missing data for required field."
                    ],
                    "recipe_name": [
                        "Missing data for required field."
                    ]
                }
            },
            "status": "Unprocessable Entity"
        }

        assert_recipe_update(
            client=client, 
            expected_response=expected_response, 
            recipe_id='abc123-format-of-uuid-invalid', 
            updated_recipe=updated_recipe, 
            expected_status = 422
        )
        
    
    
    def test_put_recipe_by_id_duplicate_name(self, client, seeded_recipes):
        recipe = seeded_recipes[0] # recipe to update
        recipe_two = seeded_recipes[1] # recipe to use existing name of
        updated_recipe = {
            "recipe_name": recipe_two.recipe_name, # apply the same name as another recipe
            "instructions": recipe.instructions,
            "notes": recipe.notes
        }

        expected_response =  {
            "code": 400,
            "message": "Recipe name already in use, name must be unique",
            "status": "Bad Request"
        }

        assert_recipe_update(
            client=client, 
            expected_response=expected_response, 
            recipe_id=str(recipe.id), 
            updated_recipe=updated_recipe, 
            expected_status = 400
        )

