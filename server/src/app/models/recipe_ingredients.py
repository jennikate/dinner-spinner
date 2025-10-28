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

class RecipeIngredient(db.Model):
    """
    SQLAlchemy model for the recipe_ingredient table

    :amount: The amount of the ingredient
    """
    __tablename__ = 'recipe_ingredients'

    id = db.Column(Uuid(), primary_key=True, default=uuid4)
    amount = db.Column(db.Float, nullable=False)

    recipe_id = db.Column(db.UUID, db.ForeignKey('recipes.id', ondelete="CASCADE"))
    ingredient_id = db.Column(db.UUID, db.ForeignKey('ingredients.id'))
    unit_id = db.Column(db.UUID, db.ForeignKey('units.id'))

    # We copy these over so if a user deletes an ingredient later it doesn't break existing recipes
    # They can come and update these fields as part of updating ingredients on a recipe
    ingredient_name = db.Column(db.String, nullable=False) # copied from ingredient table to preserve name at time of recipe creation
    unit_name = db.Column(db.String, nullable=False) # copied from unit table to preserve name at time of recipe creation

    recipe = db.relationship('Recipe', back_populates='recipe_ingredients')
    ingredient = db.relationship('Ingredient', back_populates='recipe_ingredients')
    unit = db.relationship('Unit', back_populates='recipe_ingredients')


    def __repr__(self):
        return f"<RecipeIngredient: {self.amount} {self.unit.unit_name} of {self.ingredient.ingredient_name}>"
