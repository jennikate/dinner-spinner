# =====================================
#  Imports
# =====================================

import pytest

from ....fixtures import base_recipe

# =====================================
#  Body
# =====================================

class TestPostRecipeWithErrors:
    def test_post_recipe_missing_fields(self, client):
        payload = {}
        response = client.post("/v1/recipes", json=payload)
        data = response.get_json()

        expected_response = {
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

        assert response.status_code == 422
        assert data == expected_response

    def test_post_recipe_null_ingredient(self, client, base_recipe):
        """
        Tests only the required fields are sent.
        """
        data_to_post = {
            **base_recipe, # unpack (spread operator)
            "notes": None,
            "ingredients": [
                { "ingredient_name": None },
            ]
        }

        response = client.post("/v1/recipes", json=data_to_post)
        response_data = response.get_json()

        expected_response = {
            "code": 422,
            "errors": {
                "json": {
                    "ingredients": {
                        "0": {
                            "amount": [
                                "Missing data for required field."
                            ],
                            "unit_id": [
                                "Missing data for required field."
                            ],
                            "ingredient_name": [
                                "Field may not be null."
                            ]
                        }
                    }
                }
            },
            "status": "Unprocessable Entity"
        }

        assert response.status_code == 422
        print(f"response -> {response_data}")
        assert response_data == expected_response

    # def test_post_recipe_short_ingredient(self, client, base_recipe):
    #     """
    #     Tests only the required fields are sent.
    #     """
    #     data_to_post = {
    #         **base_recipe, # unpack (spread operator)
    #         "notes": None,
    #         "ingredients": [
    #             { "ingredient_name": "" },
    #         ]
    #     }

    #     response = client.post("/v1/recipes", json=data_to_post)
    #     response_data = response.get_json()

    #     expected_response = {
    #         "code": 422,
    #         "errors": {
    #             "json": {
    #                 "ingredients": {
    #                     "0": {
    #                         "ingredient_name": [
    #                             "Field may not be null."
    #                         ]
    #                     }
    #                 }
    #             }
    #         },
    #         "status": "Unprocessable Entity"
    #     }

    #     assert response.status_code == 422
    #     assert response_data == expected_response

    
    # def test_post_recipe_long_ingredient(self, client, base_recipe):
    #     """
    #     Tests only the required fields are sent.
    #     """
    #     data_to_post = {
    #         **base_recipe, # unpack (spread operator)
    #         "notes": None,
    #         "ingredients": [
    #             { "ingredient_name": "I am longer than sixty four characters. I am longer than sixty four characters" }
    #         ]
    #     }

    #     response = client.post("/v1/recipes", json=data_to_post)
    #     response_data = response.get_json()

    #     expected_response = {
    #         "code": 422,
    #         "errors": {
    #             "json": {
    #                 "ingredients": {
    #                     "0": {
    #                         "ingredient_name": [
    #                             "Field may not be null."
    #                         ]
    #                     }
    #                 }
    #             }
    #         },
    #         "status": "Unprocessable Entity"
    #     }

    #     assert response.status_code == 422
    #     assert response_data == expected_response


    def test_post_recipe_invalid_instruction_keys(self, client):
        payload = {
            "recipe_name": "My simple recipe",
            "instructions": [
                {
                "bad": 1,
                "key": "First thing you do is"
                },
                {
                "bad": 2,
                "key": "Second thing you do is"
                }
            ]
        } 

        response = client.post("/v1/recipes", json=payload)
        data = response.get_json()

        expected_response = {
            "code": 422,
            "errors": {
                "json": {
                    "instructions": {
                        "0": {
                            "bad": [
                                "Unknown field."
                            ],
                            "instruction": [
                                "Missing data for required field."
                            ],
                            "key": [
                                "Unknown field."
                            ],
                            "step_number": [
                                "Missing data for required field."
                            ]
                        },
                        "1": {
                            "bad": [
                                "Unknown field."
                            ],
                            "instruction": [
                                "Missing data for required field."
                            ],
                            "key": [
                                "Unknown field."
                            ],
                            "step_number": [
                                "Missing data for required field."
                            ]
                        }
                    }
                }
            },
            "status": "Unprocessable Entity"
        }

        assert response.status_code == 422
        assert data == expected_response


    def test_post_recipe_missing_instruction_keys(self, client):
        payload = {
            "recipe_name": "My simple recipe",
            "instructions": [
                {
                "step_number": 1
                },
                {
                "instruction": "Second thing you do is"
                }
            ]
        } 

        response = client.post("/v1/recipes", json=payload)
        data = response.get_json()

        expected_response = {
            "code": 422,
            "errors": {
                "json": {
                    "instructions": {
                        "0": {
                            "instruction": [
                                "Missing data for required field."
                            ]
                        },
                        "1": {
                            "step_number": [
                                "Missing data for required field."
                            ]
                        }
                    }
                }
            },
            "status": "Unprocessable Entity"
        }

        assert response.status_code == 422
        assert data == expected_response


    def test_post_recipe_invalid_types(self, client):
        payload = {
            "recipe_name": 1,
            "instructions": [
                {
                "step_number": "bob",
                "instruction": 1
                }
            ]
        } 
        
        response = client.post("/v1/recipes", json=payload)
        data = response.get_json()

        expected_response = {
            "code": 422,
            "errors": {
                "json": {
                    "instructions": {
                        "0": {
                            "step_number": [
                                "Not a valid integer."
                            ],
                            "instruction": [
                                "Not a valid string."
                            ]
                        }
                    },
                    "recipe_name": [
                        "Not a valid string."
                    ]
                }
            },
            "status": "Unprocessable Entity"
        }

        assert response.status_code == 422
        assert data == expected_response

    
    def test_post_name_too_long(self, client, base_recipe):
        new_recipe = {
            **base_recipe,
            "recipe_name": "Beef burgers with side salad and coleslaw, Beef burgers with side salad and coleslaw"
        }
        response = client.post("/v1/recipes", json=new_recipe)
        data = response.get_json()

        expected_response = {
            "code": 422,
            "errors": {
                "json": {
                    "_schema": [
                        "recipe_name must not exceed 64 characters."
                    ]
                }
            },
            "status": "Unprocessable Entity"
        }

        assert response.status_code == 422
        assert data == expected_response


    def test_post_name_empty_string(self, client, base_recipe):
        new_recipe = {
            **base_recipe,
            "recipe_name": ""
        }
        response = client.post("/v1/recipes", json=new_recipe)
        data = response.get_json()

        expected_response = {
            "code": 422,
            "errors": {
                "json": {
                    "_schema": [
                        "Name must not be empty."
                    ]
                }
            },
            "status": "Unprocessable Entity"
        }

        assert response.status_code == 422
        assert data == expected_response


@pytest.mark.usefixtures("seeded_recipes")
class TestPostRecipeWhenExists:
    def test_post_recipe_already_exists(self, client, base_recipe):
        response = client.post("/v1/recipes", json=base_recipe)
        data = response.get_json()

        expected_response = {
            'code': 422, 
            'errors': {
                'json': {
                    'recipe_name': [
                        'There is already a recipe with name: My simple recipe.'
                    ]
                }
            }, 
            'status': 'Unprocessable Entity'
        }

        assert response.status_code == 422
        assert data == expected_response

