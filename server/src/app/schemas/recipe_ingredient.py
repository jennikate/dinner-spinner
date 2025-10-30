"""
This defines the Marshmallow schemas for ingredients for the API.
"""
# =====================================
# Imports
# =====================================

from marshmallow import Schema, ValidationError, fields, validates

from ..constants import MAX_PER_PAGE
from ..extensions import db as _db
from ..models.ingredients import Ingredient, IngredientType
from ..models.recipe_ingredients import RecipeIngredient
from .ingredients import IngredientTypeSchema


# =====================================
# Body
# =====================================

# ------------------
# RECIPE INGREDIENTS
# ------------------


class RecipeIngredientCreateSchema(IngredientTypeSchema):
    class Meta:
        model = RecipeIngredient
        load_instance = True
        include_fk = True
        include_relationships = False   # stop Marshmallow automatically adding nested fields from the model, let me control this & serialization

    amount = fields.Float(
        required=True,
        metadata={
            "description": "The amount of the ingredient",
            "example": "1.5"
        }
    )
    unit_id = fields.UUID(
        required=True, 
        metadata={
            "description": "The id of the unit for this ingredient",
            "example": "id=<uuid>, which relates to teaspoon"
        }
    )
    
