"""
This defines the Marshmallow schemas for generic cases for the API.
"""
# =====================================
# Imports
# =====================================

from marshmallow import Schema, fields, validates_schema


# =====================================
# Body
# =====================================

class MessageSchema(Schema):
    message = fields.String(required=True, metadata={"example": "Item deleted successfully"})


class ErrorSchema(Schema):
    status = fields.Int(
        required=True, 
        metadata={
            "example": 400,
            "description": "HTTP status code of the error"
        }
    )
    error = fields.Str(
        required=True,
        metadata={
            "example": "Bad Request",
            "description": "Short error type or reason"
        }
    )
    message = fields.Str(
        required=True,
        metadata={
            "example": "Recipe name already in use",
            "description": "Detailed explanation of the error"
        }
    )

    class Meta:
        description = "Standard error response schema"

