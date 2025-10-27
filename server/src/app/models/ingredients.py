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

# NOTE NOTE : IngredientType is not implemented other than the model
# It's currently optional on the Ingredient model
# and will not be implemented in v0.1
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
