"""
flask-smorest endpoints.

/recipes
- POST a new recipe
- GET one or all recipes
- PUT a recipe
- DELETE a recipe
"""

# =====================================
#  Imports
# =====================================

from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import asc
from sqlalchemy.exc import SQLAlchemyError # to catch db errors
from uuid import UUID

from ...extensions import db
from ...models.recipes import Recipe
from ...schemas.recipes import BaseRecipeSchema, MessageSchema, RecipeResponseSchema, RecipeUpdateSchema

# =====================================
#  Body
# =====================================

blp = Blueprint("recipe", __name__, url_prefix="/v1", description="Operations on recipes")


@blp.route("/recipes")
class RecipeResource(MethodView):
    @blp.arguments(BaseRecipeSchema)
    @blp.response(201, BaseRecipeSchema)
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


    # @blp.arguments(RecipeArgsSchema, location="query") -> will be used for tags
    @blp.response(200, RecipeResponseSchema(many=True))
    def get(self):
        """
        Get recipes
        """
        current_app.logger.debug("---------- Starting Get Recipes ----------")
        # current_app.logger.debug(f"Getting jobs with args: {args}")

        # create the base query in lazy state (hasn't hit db yet)
        # this allows us to conditionally add filters to it
        # before running
        # No SQL is sent to the database until you call something like .all(), .first(), .count(), etc.
        query = Recipe.query

        # Apply default sort by name
        recipes = query.order_by(Recipe.recipe_name.asc()).all()
        current_app.logger.debug(f"Number recipes retrieved: {len(recipes)}")
        current_app.logger.debug(f"Recipes retrieved: {recipes}")
        
        current_app.logger.debug("---------- Finished Get Recipes ----------")
        return recipes
    
@blp.route("/recipes/<recipe_id>")
class RecipeResource(MethodView):
    @blp.response(200, RecipeResponseSchema)
    def get(self, recipe_id):
        """
        Get recipe by id
        """
        current_app.logger.debug("---------- Starting Get Recipes by ID ----------")
        current_app.logger.debug(f"Getting recipe with id: {recipe_id}")

        try:
            recipe_uuid = UUID(recipe_id)  # converts string to UUID object
        except ValueError:
            abort(400, message="Invalid recipe id")

        recipe = db.session.get(Recipe, recipe_uuid)
        if not recipe:
            abort(404, message="Recipe not found")

        current_app.logger.debug(f"Recipe retrieved: {recipe}")
        
        current_app.logger.debug("---------- Finished Get Recipes by ID ----------")
        return recipe
    

    @blp.arguments(BaseRecipeSchema)
    @blp.response(200, RecipeResponseSchema)
    def put(self, update_data, recipe_id):
        """
        Update recipe by id
        """
        current_app.logger.debug("---------- Starting Put Recipes by ID ----------")
        current_app.logger.debug(f"Updating recipe id: {recipe_id}")
        current_app.logger.debug(f"Updating recipe with: {update_data}")

        try:
            recipe_uuid = UUID(recipe_id)  # converts string to UUID object
        except ValueError:
            abort(400, message="Invalid recipe id")

        recipe = db.session.get(Recipe, recipe_uuid)
        if not recipe:
            abort(404, message="Recipe not found")

        # Pass current recipe_id to schema context for validation
        schema = RecipeUpdateSchema(context={"recipe_id": recipe_id})
        validated_data = schema.load(update_data)  # runs all validations

        try:
            # validation is set on the schema and run via the 
            # @blp.arguements command, erroring out before
            # code reaches here
            recipe = Recipe(**validated_data)
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
        current_app.logger.debug("---------- Finished Put Recipes by ID ----------")
        
        return recipe
        

    
    @blp.response(200, MessageSchema)
    def delete(self, recipe_id):
        """
        Delete recipe
        """
        current_app.logger.debug("---------- Starting Delete Recipes by ID ----------")
        current_app.logger.debug(f"Getting jobs with id: {recipe_id}")

        try:
            recipe_uuid = UUID(recipe_id)
        except ValueError:
            abort(400, message="Invalid recipe id")

        recipe = db.session.get(Recipe, recipe_uuid)
        if not recipe:
            abort(404, message="Recipe not found")

        try:
            db.session.delete(recipe)
            db.session.commit()
        except SQLAlchemyError as sqle:
            db.session.rollback()
            current_app.logger.error(f"SQLAlchemyError writing to db: {str(sqle)}")
            abort(500, message=f"An error occurred writing to the db")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Exception writing to db: {str(e)}")
            abort(500, message=f"An error occurred writing to the db")

        current_app.logger.debug(f"Recipe deleted: {recipe_id}")
        
        current_app.logger.debug("---------- Finished Delete Recipes by ID ----------")
        return { "message": f"recipe id {recipe_id} deleted" }, 200
