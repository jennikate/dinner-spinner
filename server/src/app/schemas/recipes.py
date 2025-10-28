"""
This defines the Marshmallow schemas for recipes for the API.
"""
# =====================================
# Imports
# =====================================

from marshmallow import Schema, ValidationError, fields, validates_schema
from marshmallow_sqlalchemy import auto_field

from ..constants import MAX_PER_PAGE
from ..extensions import db as _db
from ..models.recipes import Recipe
from ..models.recipe_ingredients import RecipeIngredient
from .ingredients import BaseIngredientSchema


# =====================================
# RECIPES
# =====================================

# ------------------
# BASE
# ------------------

class InstructionSchema(Schema):
    step_number = fields.Int(required=True)
    instruction = fields.Str(required=True)


class BaseRecipeSchema(Schema):
    class Meta:
        model = Recipe
        load_instance = True
        include_fk = True  # there are fks

    id = fields.UUID(dump_only=True, data_key="recipe_id")
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
        required=False,
        allow_none=True,
        metadata={
            "description": "The name of the recipe", 
            "example": "Beef Goulash"
        }
    )
    ingredients = fields.List(
        fields.Nested(BaseIngredientSchema),
        required=False
    )

    # validates_schema runs after all fields are deserialized, so instructions can be a nested list safely.
    @validates_schema
    def validate_recipe_name(self, data, **kwargs):
        """
        Ensure recipe_name is valid.
        """
        name = data.get("recipe_name")
        if not name.strip():
            raise ValidationError("Name must not be empty.")
        
        if len(name) > 64:
            raise ValidationError("recipe_name must not exceed 64 characters.")

    # def validate_instructions(self, data, **kwargs):
    #     instructions = data.get("instructions", [])
    #     if not instructions:
    #         raise ValidationError("Instructions cannot be empty", "instructions")

    #     expected_step = 1
    #     for instr in instructions:
    #         if instr["step_number"] != expected_step:
    #             raise ValidationError(
    #                 f"Step numbers must start at 1 and increment by 1. Found {instr['step_number']}",
    #                 "instructions"
    #             )
    #         if not instr["instruction"].strip():
    #             raise ValidationError("Instruction text cannot be empty", "instructions")
    #         expected_step += 1


# ------------------
# QUERIES
# ------------------       
class RecipeQuerySchema(Schema):
    page = fields.Int(
        load_default=1, # used if page is not in request
        metadata={
            "description§": "Page number for pagination (1-indexed)",
            "example": 1
        }
    )      
    per_page = fields.Int(
        load_default=int(MAX_PER_PAGE), # used if per_page is not in request
        metadata={
            "description": "Number of results per page",
            "example": 10
        }
    )


# ------------------
# Create, Update
# ------------------
      
class RecipeCreateSchema(BaseRecipeSchema):
    @validates_schema
    def validate_unique_name(self, data, **kwargs):
        """
        Ensure recipe_name is unique in SQLite.
        """
        name = data.get("recipe_name")
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


class RecipeUpdateSchema(BaseRecipeSchema):
    """
    We have a specific update schema to allow a PUT method
    Where the name can remain the same during an update process
    As part of update if the update_recipe has a new name
    We do a validation check in the resource (route/recipe)
    and reject it if an existing recipe aleady has that name
    NOTE: for POST method we do the validation in the RecipeCreateSchema
    """
    class Meta:
        model = Recipe
        load_instance = True 


# ------------------
# RETURN client facing
# ------------------
# The Base schema is designed for public use
# so it excludes excess ID's that a client does
# not need to know about
class BaseRecipeIngredientSchema(Schema):
    class Meta:
        model = RecipeIngredient
        load_instance = True

    amount = fields.Float(
        required=True,
        metadata={
            "description": "The amount of the ingredient",
            "example": "1.5"
        }
    )

    # Rather than including (nesting) everything from the BaseIngredientSchema
    # We can use the lambda Function to include just the fields we want
    # from the model
    ingredient_name = fields.Function(lambda obj: obj.ingredient.ingredient_name)


class RecipeResponseSchema(BaseRecipeSchema):
    class Meta:
        model = Recipe
        load_instance = True 
        # return an SQLAlchemy model instance instead of a plain dictionary
        # So when I deserialize JSON with this schema, give me a Recipe object, not a Python dict.
    
    # Include the nested RecipeIngredient data
    recipe_ingredients = fields.Nested(BaseRecipeIngredientSchema, many=True)
    # ingredients = fields.Nested(BaseRecipeIngredientSchema, many=True)


# ------------------
# RETURN internal
# ------------------
# The internal schema includes all fields from models esp. IDs
# Which we need internally to Update & Delete on association tables
class InternalRecipeIngredientSchema(BaseRecipeSchema):
    class Meta:
        model = RecipeIngredient
        load_instance = True

    id = fields.UUID(
        dump_only=True,
        data_key="association_table_id"
    )
    amount = fields.Float(
        required=True,
        metadata={
            "description": "The amount of the ingredient",
            "example": "1.5"
        }
    )
    
    ingredient = fields.Nested(BaseIngredientSchema)
    # unit = fields.Nested(UnitSchema)


class InternalRecipeResponseSchema(BaseRecipeSchema):
    class Meta:
        model = Recipe
        load_instance = True 

    # Include the FULL RecipeIngredient data by using the Internal schema
    recipe_ingredients = fields.Nested(InternalRecipeIngredientSchema, many=True)
    # ingredients = fields.Nested(InternalRecipeIngredientSchema, many=True)

