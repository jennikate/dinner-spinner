"""
Tests for randomly returning recipes.
"""

# =====================================
#  Imports
# =====================================

import pytest

from src.app.constants import DEFAULT_RANDOM_RECIPES


# =====================================
#  Body
# =====================================

@pytest.mark.usefixtures("large_seeded_recipes")
class TestReturnRandomRecipesDataErrors:
    def test_invalid_amount_requested(self, client):
        data_to_post = {
            "number": 'string'
        }
        response = client.post("/v1/random", json=data_to_post)
        data = response.get_json()

        assert response.status_code == 422
        
        expected_response = {
            "code": 422,
            "errors": {
                "json": {
                    "number": [
                        "Not a valid integer."
                    ]
                }
            },
            "status": "Unprocessable Entity"
        }

        assert data == expected_response


    def test_0_requested_returns_default(self, client):
        """
        Tests the amount returned is as specified
        """
        data_to_post = {
            "number": 0, # is treated as falsey therefore DEFAULT kicks in
        }
        response = client.post("/v1/random", json=data_to_post)
        data = response.get_json()

        assert response.status_code == 200
        assert len(data) == DEFAULT_RANDOM_RECIPES

    
    def test_invalid_pin_uuid(self, client):
        data_to_post = {
            "pin": [
                "invalid_uuid"
            ]
        }
        response = client.post("/v1/random", json=data_to_post)
        data = response.get_json()

        assert response.status_code == 422
        
        expected_response = {
            "code": 422,
            "errors": {
                "json": {
                    "pin": {
                        "0": [
                            "Not a valid UUID."
                        ]
                    }
                }
            },
            "status": "Unprocessable Entity"
        }

        assert data == expected_response

    
    def test_invalid_pin_list(self, client):
        data_to_post = {
            "pin": "123"
        }
        response = client.post("/v1/random", json=data_to_post)
        data = response.get_json()

        assert response.status_code == 422
        
        expected_response = {
            "code": 422,
            "errors": {
                "json": {
                    "pin": [
                        "Not a valid list."
                    ]
                }
            },
            "status": "Unprocessable Entity"
        }

        assert data == expected_response


    def test_valid_uuid_but_doesnt_exist(self, client, large_seeded_recipes):
        data_to_post = {
            "pin": [
                large_seeded_recipes[35].id,
                "11111111-aaaa-bbbb-cccc-111111111111",
                "11111112-aaaa-bbbb-cccc-111111111112"
            ]
        }
        response = client.post("/v1/random", json=data_to_post)
        data = response.get_json()

        assert response.status_code == 404

        expected_response = {
            "code": 404,
            "message": "You have invalid recipe IDs: [UUID('11111111-aaaa-bbbb-cccc-111111111111'), UUID('11111112-aaaa-bbbb-cccc-111111111112')]",
            "status": "Not Found"
        }

        assert data == expected_response

