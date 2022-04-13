# This file is dedicated to fetching a summary of products and converting product dictionaries into these product
# summaries. Can also save these product summaries as validation set in specified files.

import json


def valuation_values_formatted_query(amount):
    """
    Takes a desired amount as input. Returns an SQL query that fetches a product info summary for every product
    in the specified number of given products.
    """
    return """SELECT product__id, product_name, category, sub_category, sub_sub_category, sub_sub_sub_category 
    FROM products 
    WHERE product__id IN ({});""".format(','.join(['%s'] * amount))


def get_validation_dict(products, sql_cursor):
    """
    Takes one or more product id(s) (str) and an SQL cursor as input. Fetches the product info summary for every product
    and places this summary in a dictonary for every products. Places these dictionaries in a list and returns this
    (list) [{}].
    """
    if not products:
        return list()
    query = valuation_values_formatted_query(len(products))
    sql_cursor.execute(query, products)

    return [{'product_id': product_info[0],
      'name': product_info[1],
      'category': product_info[2],
      'sub_category': product_info[3],
      'sub_sub_category': product_info[4],
      'sub_sub_sub_category': product_info[5]} for product_info in sql_cursor.fetchall()]


def samples_product_dict(sql_cursor, products, json_file):
    """
    Takes an SQL cursor, a product dictionary and the location of a json file (str) as input. Fetches the product
    info summary for every product in the product dict and saves this to a new dictionary. The keys in the product
    dictionary are also products, so a product info summary will also be fetched for the keys.
    Saves this new dictionary to the specified json file.
    """
    products_with_data = {}

    for mother_product, recommendations in iter(products.items()):
        products_with_data[mother_product] = {'data':
                                                  get_validation_dict((mother_product,), sql_cursor),
                                             'recommendations':
                                                 get_validation_dict(tuple(recommendations), sql_cursor)}

    save_samples(products_with_data, json_file)


def samples_other_dict(sql_cursor, products, json_file):
    """
    Takes an SQL cursor, a product dictionary and the location of a json file (str) as input. Fetches the product
    info summary for every product in the product dict and saves this to a new dictionary.
    Saves this new dictionary to the specified json file.
    """
    products_with_data = {}

    for mother_product, recommendations in iter(products.items()):
        products_with_data[mother_product] = get_validation_dict(tuple(recommendations), sql_cursor)
    save_samples(products_with_data, json_file)

    return products_with_data


def save_samples(sample_data, json_file):
    """
    Takes sample date (dict) {sample type: [product_id]} and the location of a json file (str) as input.
    Writes the sample data to the json file.
    """
    with open(json_file, 'w+') as json_open:
        json.dump(sample_data, json_open, indent=4)
