# This file is dedicated to queries, used to fetch products information out of the SQL database.

# product ids
def all_product_ids_query():
    """Returns a query that will select all product_ids in the products table."""
    return """SELECT product__id FROM products"""


def products_from_category(category_type='sub_category'):
    """
    Returns a query that will select all product_ids in a given category. You can optionally select a different based on
    a different column, by giving it to this function as a string (e.g. pass 'sub_sub_category' to filter on column
    sub_sub_category).
    """
    return """SELECT product__id FROM products WHERE {} = %s""".format(category_type)


def product_ids_in_categories():
    """Returns a query that selects all products that are in a category."""
    return """SELECT product__id FROM products WHERE category IS NOT NULL"""


# events (bought/seen together)
def event_product_query():
    """
    Returns a query that selects all product ids in the event_products table, where all products  are either looked
    at or bought together with a given product in a session. A given product_id is not returned.
    Format order is: product_id, event_type, event_type, product_id.
    """
    return """SELECT ep.product__id FROM event_products ep, sessions s, products p 
    WHERE ep.session__id = s.session__id 
    AND ep.product__id = p.product__id
    AND s.session__id in (SELECT session__id FROM event_products WHERE product__id = %s AND event_type = %s)
    AND ep.event_type = %s
    AND ep.product__id != %s;"""


# popular months
def product_pop_month_query():
    """
    Returns a query that fetches all product_ids of products that are more popular in a given month.
    !! Watch Out! Formatted with new formatting. Pass arguments with .format(). !!
    """
    # TODO: FIX month in popular_month instead of is popular_month. More are recorded.
    return """SELECT product__id FROM products WHERE popular_month LIKE '%{}%'"""


# properties
def properties_query():
    """Returns the product id and all properties of a given product, specified with product id."""
    return """SELECT product__id, sub_category, category, brand, color, flavor, doelgroep, eenheid, factor, 
        geschiktvoor, geursoort, huidconditie, huidtype, huidtypegezicht, klacht, kleur, leeftijd, soort, 
        soorthaarverzorging, soortmondverzorging, sterkte, product_type, typehaarkleuring, typetandenbostel, variant, 
        waterproof FROM products 
        WHERE product__id = %s;"""


def properties_multiple_query():
    """Returns the product ids and properties of all given products, specified with product id."""
    return """SELECT product__id, sub_category, category, brand, color, flavor, doelgroep, eenheid, factor, 
    geschiktvoor, geursoort, huidconditie, huidtype, huidtypegezicht, klacht, kleur, leeftijd, soort, 
    soorthaarverzorging, soortmondverzorging, sterkte, product_type, typehaarkleuring, typetandenbostel, variant, 
    waterproof FROM products 
    WHERE product__id IN ({});"""
