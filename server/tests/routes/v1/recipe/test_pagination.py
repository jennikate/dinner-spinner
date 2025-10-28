"""
Tests for the pagination using recipe & recipes endpoint resource in the `src.app.routes.v1/recipe_routes` module.
"""

# =====================================
#  Imports
# =====================================

import pytest

from math import ceil

from src.app.models.recipes import Recipe
from src.app.schemas.recipes import RecipeResponseSchema
from src.app.utils.paginate import paginate_query

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

        # Dump ORM objects to dicts for use in expected response
        schema = RecipeResponseSchema(many=True)
        recipes_data = schema.dump(large_seeded_recipes)  # list of dicts

        # Sort and slice for pagination
        sorted_recipes = sorted(recipes_data, key=lambda r: r["recipe_name"])
        paged_recipes = sorted_recipes[pagination_counts["recipe_number_start"]:pagination_counts["recipe_number_end"]]
        # key=lambda r: r["recipe_name"]: This is an anonymous function that takes one recipe dictionary r.
        # It returns the value of the "recipe_name" key.
        # So, sorted() will sort all the dictionaries based on the recipe_name string.

        expected_response = {
            "items": paged_recipes,
            "page": set_page, # we request page in the args above
            "pages": pagination_counts["pages"],
            "per_page": pagination_counts["per_page"],
            "total": len(large_seeded_recipes)
        }

        assert response.status_code == 200
        assert data == expected_response


@pytest.mark.usefixtures("large_seeded_recipes")
class TestPaginateQuery:
    def test_paginate_query_no_order_by(self, client, app, db, large_seeded_recipes):
        """
        Test that pagination works when order_by is not provided.
        Testing it returns the right number of items but not worried about order as no order passed.
        """
        with app.app_context():
            query = Recipe.query
            per_page = 5
            page = 2

            # Do NOT pass order_by
            result = paginate_query(query, page=page, per_page=per_page)

            assert result["page"] == page
            assert result["per_page"] == per_page
            assert result["total"] == len(large_seeded_recipes)
            assert result["pages"] == ceil(len(large_seeded_recipes) / per_page)
            assert len(result["items"]) == per_page

        