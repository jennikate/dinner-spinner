"""
This defines the Marshmallow schemas for recipes for the API.
"""
# =====================================
# Imports
# =====================================

from marshmallow import Schema, ValidationError, fields, validates, validates_schema
from sqlalchemy import select

from ..extensions import db as _db
from ..models.recipes import Recipe


# =====================================
# Body
# =====================================

class MessageSchema(Schema):
    message = fields.String(required=True, metadata={"example": "Item deleted successfully"})


# ------------------
# RECIPES
# ------------------

class InstructionSchema(Schema):
    step_number = fields.Int(required=True)
    instruction = fields.Str(required=True)

class RecipeSchema(Schema):
    id = fields.UUID(dump_only=True)
    recipe_name = fields.Str(
        required=True, 
        metadata={
            "description": "The name of the recipe", 
            "example": "Beef Goulash"
        }
    )
    instructions = fields.List(
        fields.Nested(InstructionSchema),
        required=True, 
        metadata={
            "description": "Step by step instructions in JSON with a key for step_number, and a key for instruction", 
            "example": '{"step_number": "1", "instruction": "Dice the beef"}'
        }
    )  # accepts any JSON object
    notes = fields.Str(
        metadata={
            "description": "The name of the recipe", 
            "example": "Beef Goulash"
        }
    )

    # validates_schema runs after all fields are deserialized, so instructions can be a nested list safely.
    @validates_schema
    def validate_unique_recipe_name(self, data, **kwargs):
        """
        Ensure recipe_name is valid and unique in SQLite.
        """
        name = data.get("recipe_name")
        if not name.strip():
            raise ValidationError("Name must not be empty.")
        
        if len(name) > 64:
            raise ValidationError("recipe_name must not exceed 64 characters.")

        exists_flag = _db.session.query(
            _db.session.query(Recipe)
            .filter(Recipe.recipe_name.ilike(name))  # ilike() ensures case-insensitive comparison in SQLite
            .exists()
        ).scalar()

        if exists_flag:
            raise ValidationError(
                f"There is already a recipe with name: {name}.", field_name="recipe_name"
            )
            # field_name="recipe_name" attaches the error to the correct field in the Marshmallow error response.
