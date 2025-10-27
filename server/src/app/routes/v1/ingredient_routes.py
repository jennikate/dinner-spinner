"""
flask-smorest endpoints.

/ingredients
- POST a new recipe
- GET one or all recipes
- PUT a recipe
- DELETE a recipe
"""

# =====================================
#  Imports
# =====================================

from flask import current_app, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import asc, exists
from sqlalchemy.exc import SQLAlchemyError # to catch db errors
from uuid import UUID

from ...constants import MAX_PER_PAGE
from ...extensions import db
from ...models.ingredients import Ingredient
from ...models.recipes import Recipe
from ... schemas.generic import ErrorSchema, MessageSchema
from ...schemas.ingredients import IngredientCreateSchema, IngredientResponseSchema
from ...schemas.recipes import RecipeCreateSchema, RecipeQuerySchema, RecipeResponseSchema, RecipeUpdateSchema

# For manually doing pagination without smorest see this helper function
# currently am using smorest but keeping function for reference on how it works
from ...utils.paginate import paginate_query

# =====================================
#  Body
# =====================================

blp = Blueprint("ingredient", __name__, url_prefix="/v1", description="Operations on ingredients")


@staticmethod
def add_ingredients(ingredients):
    """
    Adds new ingredients to the database if they don't already exist,
    and returns a list of ingredient IDs.
    """
    current_app.logger.debug("---------- Starting Add Ingredient Method ----------")
    current_app.logger.debug(f"Getting ids for -> {ingredients}")
    ingredients_to_return = []

    # map over ingredients and check if it has an id
    for ingredient_data in ingredients:
        current_app.logger.debug(f"Checking -> {ingredient_data}")
        # use .get id here because not all ingredients have this key
        # if we use ingredient["id"] it will return a key error when the key doesn't exist
        ingredient_id = ingredient_data.get("id")
        current_app.logger.debug(f"ID returned -> {ingredient_id}")

        # only if it exists can we append it to the list, otherwise we treat it as a new ingredient
        if ingredient_id and Ingredient.query.get(ingredient_id):
            existing = Ingredient.query.get(ingredient_id)
            current_app.logger.debug(f"Existing true so adding id -> {existing.id}")
            ingredients_to_return.append(existing)
        else:
            # add ingredient to database and get its UUID for use on recipe
            # ingredient_data from the recipe includes amount and unit that is not stored on the ingredient table
            # so we need to remove these keys before creating the Ingredient object
            ingredient_data.pop("amount", None)
            ingredient_data.pop("unit", None)
            ingredient = Ingredient(**ingredient_data)
            current_app.logger.debug(f"Adding new ingredient to database -> {ingredient}")

            try:
                db.session.add(ingredient)
                db.session.commit()
            except SQLAlchemyError as sqle:
                db.session.rollback()
                current_app.logger.error(f"SQLAlchemyError writing to db: {str(sqle)}")
                abort(500, message=f"An error occurred writing to the db")
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f"Exception writing to db: {str(e)}")
                abort(500, message=f"An error occurred writing to the db")

            current_app.logger.debug(f"Added -> {ingredient.id}")
            ingredients_to_return.append(ingredient)
    
    current_app.logger.debug("---------- Finished Add Ingredient Method ----------")
    return ingredients_to_return
