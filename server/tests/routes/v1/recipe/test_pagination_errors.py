"""
Tests for the pagination using recipe & recipes endpoint resource in the `src.app.routes.v1/recipe_routes` module.
"""

# =====================================
#  Imports
# =====================================

import pytest

from src.app.constants import MAX_PER_PAGE
from src.app.schemas.recipes import RecipeResponseSchema

from ....helpers import get_pagination_counts


# =====================================
#  Body
# =====================================

@pytest.mark.usefixtures("large_seeded_recipes")
class TestGetRecipePaginationErrors: 
    def test_request_per_page_over_max(self, client, app, db, large_seeded_recipes):
        set_page = 1
        set_per_page = MAX_PER_PAGE + 10  # Requesting over the max
        pagination_counts = get_pagination_counts(app, db, page=set_page, per_page=set_per_page)
        response = client.get(f"/v1/recipes?page={set_page}&per_page={set_per_page}")
        data = response.get_json()

        schema = RecipeResponseSchema(many=True)
        recipes_data = schema.dump(large_seeded_recipes)  # list of dicts

        mapped_recipes = [
            {
                **recipe, # unpack -> list of dicts, one per Recipe object
                "id": recipe["id"], # UUID is generated
                "notes": recipe["notes"]
            } for recipe in sorted(recipes_data, key=lambda r: r["recipe_name"])
        ]

        expected_response = {
            "items": mapped_recipes[pagination_counts["recipe_number_start"]:pagination_counts["recipe_number_end"]], # second page only
            "page": set_page, # we request page in the args above
            "pages": pagination_counts["pages"],
            "per_page": pagination_counts["per_page"],
            "total": len(large_seeded_recipes)
        }

        assert response.status_code == 200
        assert data == expected_response

    
    def test_request_pages_over_max(self, client, app, db, large_seeded_recipes):
        set_page = 800
        set_per_page = MAX_PER_PAGE
        pagination_counts = get_pagination_counts(app, db, page=set_page, per_page=set_per_page)
        response = client.get(f"/v1/recipes?page={set_page}&per_page={set_per_page}")
        data = response.get_json()

        schema = RecipeResponseSchema(many=True)
        recipes_data = schema.dump(large_seeded_recipes)  # list of dicts

        mapped_recipes = [
            {
                **recipe, # unpack -> list of dicts, one per Recipe object
                "id": recipe["id"], # UUID is generated
                "notes": recipe["notes"]
            } for recipe in sorted(recipes_data, key=lambda r: r["recipe_name"])
        ]

        expected_response = {
            "items": mapped_recipes[pagination_counts["recipe_number_start"]:pagination_counts["recipe_number_end"]], # second page only
            "page": set_page, # we request page in the args above
            "pages": pagination_counts["pages"],
            "per_page": pagination_counts["per_page"],
            "total": len(large_seeded_recipes)
        }

        assert response.status_code == 200
        assert data == expected_response

    
    def test_request_args_invalid(self, client, app, db, large_seeded_recipes):
        set_page = "Bob"
        set_per_page = "Jones"
        response = client.get(f"/v1/recipes?page={set_page}&per_page={set_per_page}")
        data = response.get_json()

        expected_response = {
            "code": 422,
            "errors": {
                "query": {
                    "page": [
                        "Not a valid integer."
                    ],
                    "per_page": [
                        "Not a valid integer."
                    ]
                }
            },
            "status": "Unprocessable Entity"
        }

        assert response.status_code == 422
        assert data == expected_response

