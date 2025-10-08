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


# =====================================
# Body
# =====================================

# ------------------
# INGREDIENTS
# ------------------

class BaseIngredientSchema(Schema):
    class Meta:
        model = Ingredient
        load_instance = True
        include_fk = True
        include_relationships = False   # stop Marshmallow automatically adding nested fields from the model, let me control this & serialization

    id = fields.UUID(
        metadata={
            "description": "The ingredient UUID if using an existing ingredient",
            "example": "id: 123 is 'milk'"
        }
    )
    ingredient_name = fields.Str(
        required=True,
        metadata={
            "description": "The name of the ingredient",
            "example": "Milk"
        }
    )


class IngredientTypeSchema(BaseIngredientSchema):
    class Meta:
        model = IngredientType
        load_instance = True
        include_fk = True
        include_relationships = False   # stop Marshmallow automatically adding nested fields from the model, let me control this & serialization

    type_id = fields.UUID(
        required=True, 
        load_only=True,
        metadata={
            "description": "The id of the type for this ingredient",
            "example": "id=<uuid>, which relates to fresh"
        }
    )


class IngredientCreateSchema(IngredientTypeSchema):
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
    
    @validates("ingredient_name")
    def validate_ingredient_name(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("ingredient_value must not be empty.")
        
        if len(value) > 64:
            raise ValidationError("ingredient_name must not exceed 64 characters.")

    
class IngredientResponseSchema(IngredientTypeSchema):
    class Meta:
        model = IngredientType
        load_instance = True
        include_fk = True
