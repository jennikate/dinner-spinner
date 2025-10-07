"""
Tests for the recipe & recipes endpoint resource in the `src.app.routes.v1/recipe_routes` module.
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

class TestGetAllRecipeWhenNoneExist:
    def test_get_all_recipes_when_none_exist(self, client, app, db):
        pagination_counts = get_pagination_counts(app, db)
        response = client.get("/v1/recipes")
        data = response.get_json()
        
        expected_response = {
            "items": [], 
            "page": 1, 
            "pages": pagination_counts["pages"],
            "per_page": pagination_counts["per_page"],
            "total": 0
        }

        assert response.status_code == 200
        assert data == expected_response


@pytest.mark.usefixtures("seeded_recipes")
class TestGetRecipe:
    def test_get_all_recipes(self, client, app, db, seeded_recipes):
        pagination_counts = get_pagination_counts(app, db)
        response = client.get("/v1/recipes")
        data = response.get_json()

        # recipe is a SQLAlchemy object, not a dict - this is done
        # to enable smorest/Marshmallow serialization/deserialization
        # but to map over it in the test we need to convert it back to a dict
        # and we want to do this as it's less brittle to take the expected
        # response from our seed and then add the additional fields
        # that will exist on return
        schema = RecipeResponseSchema(many=True)
        recipes_data = schema.dump(seeded_recipes)  # list of dicts

        mapped_recipes = [
            {
                **recipe, # unpack -> list of dicts, one per Recipe object
                "id": recipe["id"], # UUID is generated
                "notes": recipe["notes"]
            } for recipe in sorted(recipes_data, key=lambda r: r["recipe_name"])
        ]

        # item slice 
        # because we've passed nothing to the helper function
        # the default should -> start at 0, stop at MAX_PER_PAGE -> returns a new list containing the first MAX_PER_PAGE recipes.
        expected_response = {
            "items": mapped_recipes[pagination_counts["recipe_number_start"]:pagination_counts["recipe_number_end"]], 
            "page": 1,
            "pages": pagination_counts["pages"],
            "per_page": pagination_counts["per_page"],
            "total": len(seeded_recipes)
        }

        assert response.status_code == 200
        assert data == expected_response


    def test_get_all_with_pagination_args(self, client, app, db, seeded_recipes):
        pagination_counts = get_pagination_counts(app, db, page=2, per_page=1) # we specify 1 per page in args below
        response = client.get("/v1/recipes?page=2&per_page=1")
        data = response.get_json()

        schema = RecipeResponseSchema(many=True)
        recipes_data = schema.dump(seeded_recipes)  # list of dicts

        mapped_recipes = [
            {
                **recipe, # unpack -> list of dicts, one per Recipe object
                "id": recipe["id"], # UUID is generated
                "notes": recipe["notes"]
            } for recipe in sorted(recipes_data, key=lambda r: r["recipe_name"])
        ]

        expected_response = {
            "items": mapped_recipes[pagination_counts["recipe_number_start"]:pagination_counts["recipe_number_end"]], # second page only
            "page": 2, # we request page 2 in the args above
            "pages": pagination_counts["pages"],
            "per_page": pagination_counts["per_page"],
            "total": len(seeded_recipes)
        }

        assert response.status_code == 200
        assert data == expected_response


    def test_get_recipe_by_id(self, client, seeded_recipes):
        recipe_id = str(seeded_recipes[0].id)
        response = client.get(f"/v1/recipes/{recipe_id}")
        data = response.get_json()

        expected_response = RecipeResponseSchema().dump(seeded_recipes[0])
        # make this into a basic dict based on schema so we can assert

        assert response.status_code == 200
        assert data == expected_response
            