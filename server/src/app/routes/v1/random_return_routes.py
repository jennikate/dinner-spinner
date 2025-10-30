"""
flask-smorest endpoints.

/random
- GET list of random recipes

QueryParams
?number=4               # default to DEFAULT_RANDOM_RECIPES
?pin=uuid1,uuid2 etc.   # if none passed none are pinned
"""

# =====================================
#  Imports
# =====================================

from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import func

from ...constants import DEFAULT_RANDOM_RECIPES
from ...extensions import db
from ...models import Recipe
from ...schemas.generic import ErrorSchema
from ...schemas.recipes import RandomRecipeListRequestSchema, RandomRecipeListSchema


# =====================================
#  Body
# =====================================

blp = Blueprint("random", __name__, url_prefix="/v1", description="Querying for random recipe list")

@blp.route("/random")
class RandomRecipeListResource(MethodView):
    @blp.arguments(RandomRecipeListRequestSchema())
    @blp.response(200, RandomRecipeListSchema(many=True))
    @blp.alt_response(400, schema=ErrorSchema(), description="Bad request - invalid input")
    def post(self, args):
        """
        Posts a request for a list of random recipes
        Within the POST the request can contain a 
        -> number: the number of recipes to return
        -> pin: a list of uuids to keep and return as part of the response
        
        Returns list of ID and NAME, unpaginated
        """
        current_app.logger.debug("---------- Starting Get Random Recipes ----------")
        current_app.logger.debug(f"Getting recipes with args: {args}")

        # CHECK UUIDs AND CREATE LIST OF RECIPES TO RETURN BASED ON ARGS
        current_app.logger.debug("---> Handle pin recipe requests")
        current_app.logger.debug(f"Ids to pin: {args.get("pin")}")

        pins = args.get("pin", [])
        recipes_to_keep = []
        invalid_pins = []

        for id in pins:
            current_app.logger.debug(f"Looking for recipe: {id}")
            recipe = db.session.get(Recipe, id)
            if not recipe:
                invalid_pins.append(id)
            else:
                recipes_to_keep.append(recipe)

        if invalid_pins != []:
            abort(404, message=f"You have invalid recipe IDs: {invalid_pins}")
        
        # CALCULATE NUMBER TO RANDOMLY GENERATE
        current_app.logger.debug("---> Calculate number recipes to get")
        current_app.logger.debug(f"Pinned recipes: {recipes_to_keep}")
        number_to_return = (args.get("number") or DEFAULT_RANDOM_RECIPES) - len(recipes_to_keep)
        
        current_app.logger.debug(f"Requested: {args.get("number")}, Pinned: {len(recipes_to_keep)}, To randomly select: {number_to_return}")

        # GET THE RANDOM RECIPES
        current_app.logger.debug("---> Get random recipes")
        random_recipes = Recipe.query.order_by(func.random()).limit(number_to_return).all()
        current_app.logger.debug(f"Randomly found receipes: {random_recipes}")
        
        result = recipes_to_keep + random_recipes
        current_app.logger.debug(f"Return list: {result}")

        current_app.logger.debug("---------- Finished Get Random Recipes ----------")
        return result
