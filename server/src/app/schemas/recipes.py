"""
This defines the Marshmallow schemas for the API.
"""
# =====================================
# Imports
# =====================================

from marshmallow import Schema, fields


# =====================================
# Body
# =====================================

class MessageSchema(Schema):
    message = fields.String(required=True, metadata={"example": "Item deleted successfully"})


# ------------------
# RECIPES
# ------------------

class RecipeSchema(Schema):
    id = fields.UUID(dump_only=True)
    recipe_name = fields.Str(
        required=True, 
        metadata={
            "description": "The name of the recipe", 
            "example": "Beef Goulash"
        }
    )
    instructions = fields.Dict(
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
