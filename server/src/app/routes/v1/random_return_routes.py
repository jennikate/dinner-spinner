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
from flask_smorest import Blueprint

from ...constants import DEFAULT_RANDOM_RECIPES
from ...schemas.recipes import RandomRecipeListSchema


# =====================================
#  Body
# =====================================

blp = Blueprint("random", __name__, url_prefix="/v1", description="Querying for random recipe list")

@blp.route("/random")
class RandomRecipeListResource(MethodView):
    @blp.response(200, RandomRecipeListSchema(many=True))
    def get(self, args):
        """
        Get list of random recipes
        Returns list of ID and NAME, unpaginated
        """
        current_app.logger.debug("---------- Starting Get Random Recipes ----------")
        current_app.logger.debug(f"Getting recipes with args: {args}")

        current_app.logger.debug("---------- Finished Get Random Recipes ----------")
        
# return DEFAULT_RANDOM_RECIPES amount of random recipe IDs and NAME
# if number= in queryparam then returne NUMBER amount of random recipes IDs and NAME
# if pin= in queryparam then 
# -> check ID is a valid UUID
# -> check ID exists as a recipe.id
# -> store that ID to exclude_list
# -> create number_to_return = number/DEFAULT_RANDOM_RECIPES - len(exclude_list)
# -> return exclude_list + random_list

# recipe_schema = RecipeSchema(many=True)  # many=True because we return a list

# @blp.route("/random", methods=["GET"])
# def get_random_recipes():
#     # Query 7 random Recipe objects
#     random_recipes = Recipe.query.order_by(func.random()).limit(7).all()
#     # Serialize them using Marshmallow
#     return recipe_schema.dump(random_recipes)


# @blp.route("/random", methods=["GET"])
# def get_random_recipes():
#     excluded_ids = [1, 5, 9]  # IDs you want to exclude

#     # Query 7 random Recipe objects excluding the given IDs
#     random_recipes = (
#         Recipe.query
            # .filter(Recipe.id.notin_(excluded_ids))
#         .order_by(func.random())
#         .limit(7)
#         .all()
#     )

#     # Serialize with Marshmallow
#     return recipe_schema.dump(random_recipes)



# # Get excluded IDs from query parameters, e.g., /recipes/random?exclude=1,5,9
#     exclude_param = request.args.get("exclude", "")



# # Convert string like "1,5,9" into a list of integers
#     if exclude_param:
#         excluded_ids = [int(x) for x in exclude_param.split(",") if x.isdigit()]
#     else:
#         excluded_ids = []