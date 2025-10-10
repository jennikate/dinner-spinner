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

from flask import current_app, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import asc, exists
from sqlalchemy.exc import SQLAlchemyError # to catch db errors
from uuid import UUID

from ...constants import MAX_PER_PAGE
from ...extensions import db
from ...models.ingredients import Ingredient
from ...models.recipe_ingredients import RecipeIngredient
from ...models.recipes import Recipe
from ... schemas.generic import ErrorSchema, MessageSchema
from ...schemas.recipes import RecipeCreateSchema, RecipeQuerySchema, RecipeResponseSchema, RecipeUpdateSchema
from ...services.db_services import save_to_db

from .ingredient_routes import add_ingredients

# For manually doing pagination without smorest see this helper function
# currently am using smorest but keeping function for reference on how it works
from ...utils.paginate import paginate_query

# =====================================
#  Body
# =====================================

blp = Blueprint("recipe", __name__, url_prefix="/v1", description="Operations on recipes")


@blp.route("/recipes")
class RecipeResource(MethodView):
    # without () it normally is a class, with () it is an instance of the class
    # so blp.response(200, RecipeResponseSchema) is passing the class
    # and that can be fine because Flask-Smorest will try to instantiate it later
    # and can normalise it to an instance
    # this also works for @blp.response(201, RecipeResponseSchema)
    # HOWEVER it does not work when we add @blp.alt_response
    # because it immediately tries to build the OpenAPI spec entry and call Marshmallow internals
    # Marshmallow expects an instance (with fields defined), but gets a SchemaMeta (the Marshmallow metaclass), 
    # which is not iterable — and throws a Type error: TypeError: argument of type 'SchemaMeta' is not iterable
    # So we must instantiate the schema with () when using alt_response
    # @blp.arguments(RecipeCreateSchema)
    # @blp.response(201, RecipeResponseSchema)
    # @blp.alt_response(400, ErrorSchema(), description="Bad request - invalid input")
    # For consistency and defensive coding, I am going to always instantiate the schema with ()
    
    # We also need to use keyword for schema in alt_response
    # Flask-Smorest’s signature for alt_response() is:
    # def alt_response(self, status_code, *, schema=None, description=None, example=None, ...)
    # That means after status_code, all other arguments must be passed by name, not positionally.
    @blp.arguments(RecipeCreateSchema())
    @blp.response(201, RecipeResponseSchema())
    @blp.alt_response(400, schema=ErrorSchema(), description="Bad request - invalid input")
    def post(self, new_data):
        """
        Add a new recipe
        """
        current_app.logger.debug("---------- Starting Post Recipe ----------")

        current_app.logger.debug(f"--> Creating Recipe")
        # validation is set on the schema and run via the 
        # @blp.arguements command, erroring out before
        # code reaches here
        current_app.logger.debug(f"Recipe new_data: {new_data}")

        # Ingredients are not added to the Recipe model directly
        # so we need to pop them out of the new_data dict
        recipe_data = new_data.copy()
        recipe_data.pop("ingredients", None)

        current_app.logger.debug(f"Recipe new_data post pop: {recipe_data}")
        recipe = Recipe(**recipe_data)

        save_to_db(recipe)
        current_app.logger.debug(f"Recipe added: {recipe}")


        current_app.logger.debug("--> Checking Ingredients")
        if new_data.get("ingredients"):
            current_app.logger.debug("--> Creating Ingredients")
            ingredients_to_add = add_ingredients(new_data["ingredients"])
            current_app.logger.debug(f"ingredients to add -> {ingredients_to_add}")

        
            current_app.logger.debug("--> Creating Recipe+Ingredients Data")
            # for each ingredient_id create a RecipeIngredient entry
            for ingredient_to_add in ingredients_to_add:
                current_app.logger.debug(f"Adding ingredient to recipe_ingredient -> {ingredient_to_add}")
                
                recipe_ingredient = RecipeIngredient(
                    ingredient_id=ingredient_to_add.id, 
                    recipe_id=recipe.id,
                    amount=1.0,  # default to 1.0 for now until fully implement amount
                    unit_id=UUID("994e5e0d-790d-48ac-8e77-2a8a089b3cf2"),  # default to this for now until implement unit
                    ingredient_name=ingredient_to_add.ingredient_name, # denormalized field for easier searching
                    unit_name="teaspoon" # default to this for now until implement unit
                )

                save_to_db(recipe_ingredient)

        current_app.logger.debug("---------- Finished Post Recipe ----------")
        return recipe


    @blp.arguments(RecipeQuerySchema, location="query")
    @blp.response(200, RecipeResponseSchema(many=True))
    # @blp.paginate() # used if letting smorest handle pagination
    def get(self, args):
        """
        Get recipes

        Returns all recipes, paginated
        """
        current_app.logger.debug("---------- Starting Get Recipes ----------")
        current_app.logger.debug(f"Getting jobs with args: {args}")

        # extract pagination args
        current_app.logger.debug(f"Max per page -> {MAX_PER_PAGE}")
        page = int(args.get("page", 1)) # default to 1 if nothing provided
        current_app.logger.debug(f"Page -> {page}")
        per_page = int(args.get("per_page", MAX_PER_PAGE)) # default to max if nothing provided

        if per_page > MAX_PER_PAGE:
            per_page = MAX_PER_PAGE

        paginated_results = paginate_query(
            Recipe.query,
            page=page,
            per_page=per_page,
            order_by=Recipe.recipe_name.asc()  # default sort
        )

        current_app.logger.debug(f"Number recipes retrieved: {len(paginated_results)}")
        current_app.logger.debug(f"Recipes retrieved: {paginated_results}")
        
        current_app.logger.debug("---------- Finished Get Recipes ----------")
        return jsonify(paginated_results)
        # change back to paginated_results when I move to smorest for pagination

    
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
    

    @blp.arguments(RecipeUpdateSchema)
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

        # if recipe name changed, check that name does not already exist on another recipe
        new_name = update_data.get("recipe_name")
        if new_name and new_name != recipe.recipe_name:
            name_taken = db.session.query(
                exists().where(Recipe.recipe_name == new_name)
            ).scalar()
            # scalar -> returns the first column of the first row from the query result.
            # if no rows are found, it returns None.
            if name_taken:
                abort(400, message="Recipe name already in use, name must be unique")

        # If no aborts, then update all recipe fields
        for key, value in update_data.items(): # .items accesses the entries in the dict
            setattr(recipe, key, value)

        try:
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
