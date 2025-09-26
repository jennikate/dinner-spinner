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
    
