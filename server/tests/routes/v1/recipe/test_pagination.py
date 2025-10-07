"""
Tests for the pagination using recipe & recipes endpoint resource in the `src.app.routes.v1/recipe_routes` module.
"""

# =====================================
#  Imports
# =====================================

import pytest

from src.app.schemas.recipes import RecipeResponseSchema

from ....helpers import get_pagination_counts


# =====================================
#  Body
# =====================================

@pytest.mark.usefixtures("large_seeded_recipes")
class TestGetRecipePagination:
    
    def test_get_all_with_pagination_args(self, client, app, db, large_seeded_recipes):
        set_page = 3
        set_per_page = 9
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

