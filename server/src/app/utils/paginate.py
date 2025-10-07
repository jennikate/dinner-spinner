# =====================================
#  Imports
# =====================================

from flask import current_app
from math import ceil

from ..constants import MAX_PER_PAGE
from ..schemas.recipes import RecipeResponseSchema

# =====================================
#  Body
# =====================================

def paginate_query(query, page=1, per_page=MAX_PER_PAGE, order_by=None):
    """
    Paginate an SQLAlchemy query with optional sorting.

    Args:
        query: SQLAlchemy query object
        page: current page (1-indexed)
        per_page: number of items per page
        order_by: optional order_by clause (e.g., Model.column.asc())

    Returns:
        dict with pagination metadata and items
    """
    current_app.logger.debug("---------- Starting Pagination Query ----------")
        
    if order_by is not None:
        query = query.order_by(order_by)

    total = query.count()  # total items
    current_app.logger.debug(f"Total found -> {total}")

    items = query.offset((page - 1) * per_page).limit(per_page).all()
    current_app.logger.debug(f"items to return -> {items}")

    # offset(n)
    # -- Purpose: Skip the first n rows of the result set.
    # -- For pagination, you skip all items on previous pages.
    # -- e.g. page = 4, per_page = 5
    # -- (4 - 1) : gives the pages we've already returned (in this case pages 1,2,3)
    # -- 3 * 5 : gives us the records we've already returned (in this case 15)
    # -- so this tells us we have returned rows 1-15, and now want row 16+
    # limit(n)
    # -- Purpose: Return at most per_page rows.
    # chaining offset and limit
    # SQLAlchemy builds this into a query to return the next 5 rows after row 15
    # -- SELECT * FROM recipes
    # -- ORDER BY recipe_name ASC
    # -- LIMIT 5 OFFSET 15;
    # .all()
    # -- up to here SQLAlchemy just creates the base query in lazy state (hasn't hit db yet)
    # -- this allows us to conditionally add filters to it before running
    # -- .all() executes the query and returns a list of model instances
    # -- Until you call .all() (or .first(), .one(), etc.), the query is just a lazy builder
    
    # SERIALIZE - must serialize the model instance before returning as we're not using smorest to do it here
    schema = RecipeResponseSchema(many=True)
    serialized_items = schema.dump(items)
    current_app.logger.debug(f"serialized -> {serialized_items}")

    current_app.logger.debug("---------- Finished Pagination Query ----------")
    return {
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": ceil(total / per_page) if per_page else 1,
        "items": serialized_items,
    }
