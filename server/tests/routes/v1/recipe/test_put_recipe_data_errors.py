"""
Tests for the recipe & recipes endpoint resource in the `src.app.routes.v1/recipe_routes` module.
"""

# =====================================
#  Imports
# =====================================

import pytest

# =====================================
#  Body
# =====================================

# @pytest.mark.usefixtures("seeded_recipes")
# class TestPutRecipe:
#     def test_put_recipe_by_id_invalid_id(self, client):
#         response = client.put(f"/v1/recipes/invalid_uuid")
#         data = response.get_json()

#         expected_response =  {
#             "code": 400,
#             "message": "Invalid recipe id",
#             "status": "Bad Request"
#         }

#         assert response.status_code == 400
#         assert data == expected_response


#     def test_put_recipe_by_id_bad_uuid(self, client):
#         response = client.put(f"/v1/recipes/abc123-format-of-uuid-invalid")
#         data = response.get_json()

#         expected_response =  {
#             "code": 400,
#             "message": "Invalid recipe id",
#             "status": "Bad Request"
#         }

#         assert response.status_code == 400
#         assert data == expected_response


#     def test_put_recipe_by_id_uuid_doesnt_exist(self, client):
#         response = client.put(f"/v1/recipes/21d634fd-e75f-49a0-85be-0e6815a1daf0")
#         data = response.get_json()

#         expected_response =  {
#             "code": 404,
#             "message": "Recipe not found",
#             "status": "Not Found"
#         }

#         assert response.status_code == 404
#         assert data == expected_response

# TODO:
# put invalid data types
# put with no changes
# put with missing mandatory fields
# put where the optional field (e.g. notes) goes from having data to having no data
# put with name of other existing recipe