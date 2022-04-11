import recommendation_engines.statistics as stats


def properties_query():
    """"""
    return """SELECT product__id, sub_category, category, brand, color, flavor, doelgroep, eenheid, factor, 
        geschiktvoor, geursoort, huidconditie, huidtype, huidtypegezicht, klacht, kleur, leeftijd, soort, 
        soorthaarverzorging, soortmondverzorging, sterkte, product_type, typehaarkleuring, typetandenbostel, variant, 
        waterproof FROM products 
        WHERE product__id = %s;"""


def fetch_category_query(category_type='sub_category'):
    """"""
    return """SELECT {} FROM products WHERE product__id = %s""".format(category_type)


def difference(product_1_properties, product_2_properties):
    """"""
    difference_count = 0
    for i in range(len(product_1_properties)):
        if product_1_properties[i] != product_2_properties[i]:
            difference_count += 1
    return difference_count


def get_similars(product_id, product_properties, category_products, amount):
    """"""
    similar_properties_count = dict()
    for potential_similar_id, similar_properties in iter(category_products.items()):
        if product_id == potential_similar_id:
            continue
        similar_properties_count[potential_similar_id] = difference(product_properties, similar_properties)
    return stats.lowest_counts(similar_properties_count, amount)


def calculate_similar_products(product_id, sql_cursor):
    """"""
    # TODO: calculate similar products of 1
    pass
