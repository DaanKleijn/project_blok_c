import json


def valuation_values_formatted_query(amount_of_values):
    return """SELECT product__id, product_name, category, sub_category, sub_sub_category, sub_sub_sub_category 
    FROM products 
    WHERE product__id IN ({});""".format(','.join(['%s'] * amount_of_values))


def get_validation_dict(products, sql_cursor):
    """"""
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
    """"""
    products_with_data = {}

    for mother_product, recommendations in iter(products.items()):
        products_with_data[mother_product] = {'data':
                                                  get_validation_dict((mother_product,), sql_cursor),
                                             'recommendations':
                                                 get_validation_dict(tuple(recommendations), sql_cursor)}

    save_samples(products_with_data, json_file)
    return products_with_data


def samples_other_dict(sql_cursor, products, json_file):
    """"""
    products_with_data = {}

    for mother_product, recommendations in iter(products.items()):
        products_with_data[mother_product] = get_validation_dict(tuple(recommendations), sql_cursor)
    save_samples(products_with_data, json_file)

    return products_with_data


def save_samples(sample_data, json_file):
    """"""
    with open(json_file, 'w+') as json_open:
        json.dump(sample_data, json_open, indent=4)