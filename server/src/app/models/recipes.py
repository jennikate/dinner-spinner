###################################################################################################
#  Imports
###################################################################################################

from sqlalchemy import Uuid
from uuid import uuid4

from sqlalchemy.dialects.sqlite import JSON

from app.extensions import db

###################################################################################################
#  Body
###################################################################################################

class Recipe(db.Model):
    """
    SQLAlchemy model for the recipe table

    :recipe_name: A brief name for the recipe
    :instructions: A set of steps in JSON format each with {"step_number": "<number>", "instruction": <paragraph>}
    :notes: Optional additional string of notes the user wants to add
    """
    __tablename__ = 'recipes'

    id = db.Column(Uuid(), primary_key=True, default=uuid4)
    recipe_name = db.Column(db.String(32), nullable=False, unique=True)
    instructions = db.Column(JSON, nullable=False)
    notes = db.Column(db.String(1024), nullable=True)

    recipe_ingredients = db.relationship('RecipeIngredient', back_populates='recipe')
    # NOTES:
    # recipe_ingredients -> attribute name on current model (Recipe).
    # tells SQLAlchemy: “when I have a Recipe, I can access its related RecipeIngredient rows via .recipe_ingredients”.
    # .recipe_ingredients returns a list (technically a dynamic collection) of RecipeIngredient objects
    # each RecipeIngredient has fields like .id, .amount, .ingredient_id, etc.
    # "RecipeIngredient" -> the name of the related Python Model class (not the table name).
    # back_populates="recipe" -> links this attribute to the .recipe attribute on the RecipeIngredient model.
    # From a Recipe, you can get all its RecipeIngredient objects (via .recipe_ingredients).
    # Relationship summary: One Recipe has Many RecipeIngredient objects,
    # and Each RecipeIngredient has One Recipe.
    # HOW DOES IT 'GET'
    # When you access .recipe_ingredients, SQLAlchemy performs a lazy load query 
    # (unless configured otherwise) to fetch all RecipeIngredient rows with recipe_id = r.id.
    # It returns a Python collection (usually a list-like InstrumentedList) of RecipeIngredient model instances.
    # We serialize this into JSON in our schema's using smorest for use elsewhere.

    def __repr__(self):
        return f"<Recipe: {self.recipe_name}>"


class IngredientType(db.Model):
    """
    SQLAlchemy model for the ingredient_type table

    :type: A type that can be searched on later, e.g. store_cupboard, fresh
    """
    __tablename__ = 'ingredient_types'

    id = db.Column(Uuid(), primary_key=True, default=uuid4)
    ingredient_type = db.Column(db.String(32), nullable=False)

    ingredients = db.relationship('Ingredient', back_populates='ingredient_type')

    def __repr__(self):
        return f"<ingredient_type: {self.ingredient_type}>"


class Ingredient(db.Model):
    """
    SQLAlchemy model for the ingredient table

    :ingredient_name: The name of the ingredient
    :type: A type that can be searched on later, e.g. store_cupboard, fresh
    """
    __tablename__ = 'ingredients'

    id = db.Column(Uuid(), primary_key=True, default=uuid4)
    ingredient_name = db.Column(db.String(32), nullable=False)
    type_id = db.Column(db.UUID, db.ForeignKey('ingredient_types.id'), nullable=True)

    ingredient_type = db.relationship('IngredientType', back_populates='ingredients')
    recipe_ingredients = db.relationship('RecipeIngredient', back_populates='ingredient')

    def __repr__(self):
        return f"<Ingredient: {self.ingredient_name}>"


class Unit(db.Model):
    """
    SQLAlchemy model for the unit table

    :unit_name: The name of the unit
    :abbreviation: The common short form of the unit name
    """
    __tablename__ = 'units'

    id = db.Column(Uuid(), primary_key=True, default=uuid4)
    unit_name = db.Column(db.String(32), nullable=False)
    abbreviation = db.Column(db.String(16), nullable=True)

    recipe_ingredients = db.relationship('RecipeIngredient', back_populates='unit')

    def __repr__(self):
        return f"<unit: {self.unit_name}>"
    

class RecipeIngredient(db.Model):
    """
    SQLAlchemy model for the recipe_ingredient table

    :amount: The amount of the ingredient
    """
    __tablename__ = 'recipe_ingredients'

    id = db.Column(Uuid(), primary_key=True, default=uuid4)
    amount = db.Column(db.Float, nullable=False)

    recipe_id = db.Column(db.UUID, db.ForeignKey('recipes.id'), nullable=False)
    ingredient_id = db.Column(db.UUID, db.ForeignKey('ingredients.id'), nullable=False)
    unit_id = db.Column(db.UUID, db.ForeignKey('units.id'), nullable=False)

    recipe = db.relationship('Recipe', back_populates='recipe_ingredients')
    ingredient = db.relationship('Ingredient', back_populates='recipe_ingredients')
    unit = db.relationship('Unit', back_populates='recipe_ingredients')


    def __repr__(self):
        return f"<RecipeIngredient: {self.amount} {self.unit.unit_name} of {self.ingredient.ingredient_name}>"
