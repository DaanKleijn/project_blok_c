# This file is dedicated to comparing the properties of two products.

import recommendation_engines.frequencies as stats


def difference(product_1_properties, product_2_properties):
    """
    Takes properties of two products (tuple) as input. Counts the amount of properties that are different.
    Returns this count (dict) {product_id: difference_count}.
    """
    difference_count = 0
    for i in range(len(product_1_properties)):
        if product_1_properties[i] != product_2_properties[i]:
            difference_count += 1
    return difference_count


def get_similars(product_id, product_properties, category_products, amount):
    """
    Takes a product_id (str),
    (that same product's) product properties (tuple) (str, str ...),
    a dictionary with all products in the same category (dict) {product_id: product_properties},
    and a desired amount (int) as input.
    Counts for every product in the category dictionary, how many properties don't match.
    returns the desired amount of products that have the most matching properties
    """
    similar_properties_count = dict()
    # cycles through every product in category_products, taking the product_id and the properties.
    for potential_similar_id, similar_properties in iter(category_products.items()):
        # skips itself
        if product_id == potential_similar_id:
            continue
        # counts difference in properties and saves this to a dict. The product_id of the potential similar is the key.
        similar_properties_count[potential_similar_id] = difference(product_properties, similar_properties)
    # returns the products with the least discrepancies between properties.
    return stats.lowest_counts(similar_properties_count, amount)
