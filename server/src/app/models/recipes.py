# =====================================
#  Imports
# =====================================

from sqlalchemy import Uuid
from uuid import uuid4

from sqlalchemy.dialects.sqlite import JSON

from ..extensions import db

# =====================================
#  Body
# =====================================

class Recipe(db.Model):
    """
    SQLAlchemy model for the recipe table

    :recipe_name: A brief name for the recipe
    :instructions: A set of steps in JSON format each with {"step_number": 1, "instruction": <paragraph>}
    :notes: Optional additional string of notes the user wants to add
    """
    __tablename__ = 'recipes'

    id = db.Column(Uuid(), primary_key=True, default=uuid4)
    recipe_name = db.Column(db.String(64), nullable=False, unique=True)
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
   