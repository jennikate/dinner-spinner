"""
Common services for adding to database.
"""

# =====================================
#  Imports
# =====================================

from flask import current_app
from flask_smorest import abort
from sqlalchemy.exc import SQLAlchemyError # to catch db errors

from ..extensions import db

# =====================================
#  Body
# =====================================

@staticmethod
def save_to_db(data_to_add):
    """
    Process standard saving to the database with error handling.
    """
    try:
        db.session.add(data_to_add)
        db.session.commit()
    except SQLAlchemyError as sqle:
        db.session.rollback()
        current_app.logger.error(f"SQLAlchemyError writing to db: {str(sqle)}")
        abort(500, message=f"An error occurred writing to the db")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Exception writing to db: {str(e)}")
        abort(500, message=f"An error occurred writing to the db")
    
    return data_to_add
