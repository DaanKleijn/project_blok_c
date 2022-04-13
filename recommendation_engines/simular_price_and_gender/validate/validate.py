# This file is dedicated to creating the datasets used to validate the algorithms .

import PostgreSQL.connect_postgresql_database as sql_c
import Validation.sample_support as sample_support
import Validation.data_conversion as convert_data
from recommendation_engines.simular_price_and_gender.recommendations import simular_gender, simular_price

mandatory_validation_file_gender = 'mandatory_validation_set_gender.json'
mandatory_validation_file_price = 'mandatory_validation_set_price.json'


def random_sampling_gender(sample_type='random_samples'):
    """
    Takes an SQL cursor and optionally a sample type (str) as input. Loads the specified type of samples and fetches the
    recommendations according to the bought together algorithm. The fetched recommendations are in a list.
    Returns fetched products with the product id (dict) {product_id: [recommended_products]} {str: [str]}.
    """
    products = sample_support.load_samples(sample_type)
    result = {}
    for product in products:
        result[product] = simular_gender(product, 4)
    return result


# def random_sampling_price(sql_cursor, sample_type='random_samples'):
#     """
#     Takes an SQL cursor and optionally a sample type (str) as input. Loads the specified type of samples and fetches the
#     recommendations according to the bought together algorithm. The fetched recommendations are in a list.
#     Returns fetched products with the product id (dict) {product_id: [recommended_products]} {str: [str]}.
#     """
#     products = sample_support.load_samples(sample_type)
#     result = {}
#     for product in products:
#         result[product] = simular_price(product, 4, sql_cursor)
#     return result


def take_mandatory_sampling_gender():
    """
    Creates a validation set for the bought together algorithm with the mandatory samples. Saves the set to
    mandatory_validation_set.json.
    """
    sql_connection, sql_cursor = sql_c.connect()
    random_products = random_sampling_gender('mandatory_samples')
    convert_data.samples_product_dict(products=random_products,
                                      sql_cursor=sql_cursor,
                                      json_file=mandatory_validation_file_gender)
    sql_c.disconnect(sql_connection, sql_cursor)


# def take_mandatory_sampling_price():
#     """
#     Creates a validation set for the bought together algorithm with the mandatory samples. Saves the set to
#     mandatory_validation_set.json.
#     """
#     sql_connection, sql_cursor = sql_c.connect()
#     random_products = random_sampling_price(sql_cursor, 'mandatory_samples')
#     convert_data.samples_product_dict(products=random_products,
#                                       sql_cursor=sql_cursor,
#                                       json_file=mandatory_validation_file_price)
#     sql_c.disconnect(sql_connection, sql_cursor)


if __name__ == '__main__':
    take_mandatory_sampling_gender()
    # take_mandatory_sampling_price()
