"""
flask-smorest endpoints.

/recipe
- POST a new recipe
- GET one or all recipes
- PATCH a recipe
- DELETE a recipe
"""

# =====================================
#  Imports
# =====================================

from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError # to catch db errors

from ...extensions import db
from ...models.recipes import Recipe
from ...schemas.recipes import RecipeSchema

# =====================================
#  Body
# =====================================

blp = Blueprint("recipe", __name__, url_prefix="/v1", description="Operations on recipes")


@blp.route("/recipe")
class RecipeResource(MethodView):
    @blp.arguments(RecipeSchema)
    @blp.response(201, RecipeSchema)
    def post(self, new_data):
        """
        Add a new recipe
        """
        current_app.logger.debug("---------- Starting Post Recipe ----------")

        try:
            # validation is set on the schema and run via the 
            # @blp.arguements command, erroring out before
            # code reaches here
            current_app.logger.debug(f"Recipe new_data: {new_data}")
            recipe = Recipe(**new_data)
            db.session.add(recipe)
            db.session.commit()
        except SQLAlchemyError as sqle:
            db.session.rollback()
            current_app.logger.error(f"SQLAlchemyError writing to db: {str(sqle)}")
            abort(500, message=f"An error occurred writing to the db")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Exception writing to db: {str(e)}")
            abort(500, message=f"An error occurred writing to the db")

        current_app.logger.debug(f"Recipe added: {recipe}")

        current_app.logger.debug("---------- Finished Post Recipe ----------")
        return recipe
    