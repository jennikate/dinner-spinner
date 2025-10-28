# =====================================
#  Imports
# =====================================

from flask import current_app
from flask_smorest import abort
from uuid import UUID

from ..models.recipe_ingredients import RecipeIngredient
from ..services.db_services import save_to_db

# =====================================
#  Body
# =====================================



# def add_ingredients_to_database(ingredients):
#     """
#     For the list of ingredients
#     Check if exists in the database and if it does return that ID
#     If it does not, add to ingredients table and return the newly created ID
#     Args:
#         ingredients: Dict of ingredients with name
#         > may have id which is used here
#         > could have but isn't used here amount and unit

#     Returns:
#         on success or is aborted in add_ingredients static method
#     """
#     current_app.logger.debug("---------- Starting Save Ingredients ----------")
#     current_app.logger.debug(f"Received ingredients -> {ingredients}")
    
#     ingredients_to_add = add_ingredients(new_data["ingredients"])
            
#     current_app.logger.debug("--> Checking for ingredient failures")
#     current_app.logger.debug(f"Failed ingredients: {ingredients["failed"]}")
#     # := (walrus operator)
#     # Assign to <varfailed> whatever is in <ingredients_to_add["failed"]>, and if that value is truthy (not empty), then run the code block.”
#     if failed := ingredients["failed"]:
#         abort(
#             422,
#             message=f"Failed to create all ingredients. Review and try again. Failed: {failed}"
#         )

# def add_ingredients_to_recipe(ingredients, recipe_id):
#     """
#     Add a list of existing ingredients to an existing recipe.
#     With the amount/unit specific to this recipe. [NOTE: still to build amt/unit]

#     Args:
#         ingredients: Dict of ingredients with id, name, amount, unit
#         recipe_id: uuid of the recipe to add ingredients to

#     Returns:
#         on success or is aborted in save_to_db
#     """
#     current_app.logger.debug("---------- Starting Add Ingredients to Recipe ----------")
#     current_app.logger.debug(f"Received ingredients -> {ingredients} for recipe -> {recipe_id}")
    
#     for ingredient_to_add in ingredients:
#         current_app.logger.debug(f"Adding ingredient to recipe_ingredient -> {ingredient_to_add}")
                
#         recipe_ingredient = RecipeIngredient(
#             ingredient_id=ingredient_to_add.id, 
#             recipe_id=recipe_id,
#             amount=1.0,  # default to 1.0 for now until fully implement amount
#             unit_id=UUID("994e5e0d-790d-48ac-8e77-2a8a089b3cf2"),  # default to this for now until implement unit
#             ingredient_name=ingredient_to_add.ingredient_name, # denormalized field for easier searching
#             unit_name="teaspoon" # default to this for now until implement unit
#         )

#         save_to_db(recipe_ingredient)

#     current_app.logger.debug("---------- Finished Add Ingredients to Recipe ----------")
    
#     # if it fails to save to db, process is aborted as part of save_to_db service
#     # and should not reach "complete"
#     return
