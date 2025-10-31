"""
Services related to ingredients
"""

# =====================================
#  Imports
# =====================================

from uuid import UUID
from flask import current_app
from flask_smorest import abort
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError # to catch db errors

from ..extensions import db
from ..models import Ingredient, RecipeIngredient
from ..schemas.ingredients import IngredientResponseSchema
from ..services.db_services import DbService


# =====================================
#  Body
# =====================================

# Collecting within a class for clarity
class IngredientService:
    @staticmethod
    def save_ingredients(ingredients):
        """
        Adds new ingredients to the database if they don't already exist,
        and returns a list of ingredient IDs.
        """
        current_app.logger.debug("---------- Starting Save Ingredient Method ----------")
        current_app.logger.debug(f"Getting ids for -> {ingredients}")

        ingredients_saved = []
        ingredients_failed = []

        # map over ingredients and check if it has an id
        for ingredient_data in ingredients:
            current_app.logger.debug(f"Checking -> {ingredient_data}")

            # convert strings to lowercase, we use != so we don't try to convert UUID strings
            for key, value in ingredient_data.items():  
                if isinstance(value, str) and not isinstance(value, UUID): # isinstance check the type of value
                    ingredient_data[key] = value.lower() # set the value of the key to lowercase

            # Set the ingredient ID if it exists to a var, and the name to a var
            # use .get id here because not all ingredients have this key
            # if we use ingredient["id"] it will return a key error when the key doesn't exist
            ingredient_id = ingredient_data.get("id")
            ingredient_name = ingredient_data.get("ingredient_name")
            current_app.logger.debug(f"ID returned -> {ingredient_id}, for NAME -> {ingredient_name}")
            
            # If we have ID and it exists in the ingredient table, use that id
            if ingredient_id and Ingredient.query.get(ingredient_id):
                existing = Ingredient.query.get(ingredient_id)
                current_app.logger.debug(f"ID exists true so using id -> {existing.id}")
                ingredients_saved.append(ingredient_data)

            # If we do not have an existing ID check if the name string exists in the ingredient table, if it does use that id
            # elif ingredient_name and db.session.query(Ingredient).filter(Ingredient.ingredient_name == ingredient_name).first():
            #     existing = db.session.query(Ingredient).filter(Ingredient.ingredient_name == ingredient_name).first()
            #     current_app.logger.debug(f"Name exists so using that name's id -> {existing.id}")
            #     ingredients_saved.append(existing)
            else:
                statement = select(Ingredient).filter_by(ingredient_name=ingredient_name)
                existing = db.session.execute(statement).scalar_one_or_none()  # returns Ingredient or None

                if existing:
                    current_app.logger.debug(f"Name exists so using that {ingredient_name}'s id -> {existing.id}")
                    ingredient_data["id"] = existing.id
                    ingredients_saved.append(ingredient_data)

                else:
                    # Save ingredient to database and get its UUID for use on recipe
                    # ingredient_data from the recipe includes amount and unit that is not stored on the ingredient table
                    # we only want the ingredient name for the ingredient table
                    ingredient = Ingredient(ingredient_name=ingredient_data["ingredient_name"])
                    current_app.logger.debug(f"Adding new ingredient to database -> {ingredient}")

                    try:
                        db.session.add(ingredient)
                        db.session.commit()
                        ingredient_data["id"] = ingredient.id
                        ingredients_saved.append(ingredient_data)
                    except SQLAlchemyError as sqle:
                        db.session.rollback()
                        print(f"SQLAlchemyError writing to db: {str(sqle)}")
                        
                        current_app.logger.error(f"SQLAlchemyError writing to db: {str(sqle)}")
                        ingredients_failed.append(ingredient)
                    except Exception as e:
                        db.session.rollback()
                        current_app.logger.error(f"Exception writing to db: {str(e)}")
                        ingredients_failed.append(ingredient)

        # Once all attempted, if any failed abort and return information to client
        current_app.logger.debug("--> Checking for ingredient failures")
        current_app.logger.debug(f"Failed ingredients: {ingredients_failed}")
        if ingredients_failed!= []:
            mapped_failures = []
            for ingredient in ingredients_failed:
                schema = IngredientResponseSchema()
                mapped_failures.append(schema.dump(ingredient))
            abort(422, message=f"Failed to create all ingredients, review and try again. Failed: {mapped_failures}") 

        current_app.logger.debug(f"Returning saved -> {ingredients_saved}")
        current_app.logger.debug("---------- Finished Save Ingredient Method ----------")
        return ingredients_saved


    @staticmethod
    def add_ingredients_to_recipe(ingredients, recipe_id):
        """
        Add a list of existing ingredients to an existing recipe.
        With the amount/unit specific to this recipe. [NOTE: still to build amt/unit]

        Args:
            ingredients: Dict of ingredients with id, name, amount, unit
            recipe_id: uuid of the recipe to add ingredients to

        Returns:
            on success or is aborted in save_to_db_abort_on_fail
        """
        current_app.logger.debug("---------- Starting Add Ingredient To Recipe Method ----------")
        
        for ingredient_to_add in ingredients:
            current_app.logger.debug(f"Adding ingredient to recipe_ingredient -> {ingredient_to_add}")

            recipe_ingredient = RecipeIngredient(
                ingredient_id=ingredient_to_add["id"], 
                recipe_id=recipe_id,
                amount=ingredient_to_add["amount"],
                unit_id=ingredient_to_add["unit_id"],  # default to this for now until implement unit
                ingredient_name=ingredient_to_add["ingredient_name"],
                unit_name="teaspoon" # default to this for now until implement unit
            )

            DbService.save_to_db_abort_on_fail(recipe_ingredient)

        current_app.logger.debug("---------- Finished Add Ingredient To Recipe Method ----------")
        return
    

    @staticmethod
    def remove_ingredients_from_recipe(recipe_id):
        """
        As we use PUT methods to update recipes we expect
        the user to include all the required ingredients (existing and new)
        Therefore we need to clear all related ingredients from the recipe
        Before recreating them

        Args:
            recipe_id: uuid of the recipe to remove ingredients from

        Returns:
            on success or is aborted in save_to_db_abort_on_fail
        """

        current_app.logger.debug("---------- Starting Remove Ingredients From Recipe Method ----------")
        try:
            recipe_uuid = UUID(recipe_id)
        except ValueError:
            abort(400, message="Invalid recipe id")

        try:
            deleted = RecipeIngredient.query.filter_by(recipe_id=recipe_uuid).delete()
            db.session.commit()
            current_app.logger.debug(f"Deleted {deleted} ingredients for recipe {recipe_id}")
        except SQLAlchemyError as sqle:
            db.session.rollback()
            current_app.logger.error(f"SQLAlchemyError writing to db: {str(sqle)}")
            abort(500, message=f"An error occurred writing to the db")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Exception writing to db: {str(e)}")
            abort(500, message=f"An error occurred writing to the db")

        current_app.logger.debug("---------- Finished Remove Ingredients From Recipe Method ----------")
        return
