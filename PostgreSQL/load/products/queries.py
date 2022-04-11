# product ids
def all_product_ids_query():
    return """SELECT product__id FROM products"""


def products_from_category(category_type='sub_category'):
    """"""
    return """SELECT product__id FROM products WHERE {} = %s""".format(category_type)


def product_ids_in_categories():
    """"""
    return """SELECT product__id FROM products WHERE category IS NOT NULL"""


# popular months
def product_pop_month_query():
    """Returns a query that fetches all product_ids of products that are more popular in a given month."""
    # TODO: FIX month in popular_month instead of is popular_month. More are recorded.
    return """SELECT product__id FROM products WHERE popular_month LIKE '%{}%'"""


# properties
def properties_query():
    """"""
    return """SELECT product__id, sub_category, category, brand, color, flavor, doelgroep, eenheid, factor, 
        geschiktvoor, geursoort, huidconditie, huidtype, huidtypegezicht, klacht, kleur, leeftijd, soort, 
        soorthaarverzorging, soortmondverzorging, sterkte, product_type, typehaarkleuring, typetandenbostel, variant, 
        waterproof FROM products 
        WHERE product__id = %s;"""


def properties_multiple_query():
    """"""
    return """SELECT product__id, sub_category, category, brand, color, flavor, doelgroep, eenheid, factor, 
    geschiktvoor, geursoort, huidconditie, huidtype, huidtypegezicht, klacht, kleur, leeftijd, soort, 
    soorthaarverzorging, soortmondverzorging, sterkte, product_type, typehaarkleuring, typetandenbostel, variant, 
    waterproof FROM products 
    WHERE product__id IN ({});"""
