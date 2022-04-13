# This file is dedicated to creating the datasets used to validate the bought together algorithm.

import PostgreSQL.connect_postgresql_database as sql_c
import Validation.sample_support as sample_support
import Validation.data_conversion as convert_data
import recommendation_engines.bought_together.recommend as bought_together

random_validation_file = 'random_validation_set.json'
mandatory_validation_file = 'mandatory_validation_set.json'


def random_sampling(sql_cursor, sample_type='random_samples'):
    """
    Takes an SQL cursor and optionally a sample type (str) as input. Loads the specified type of samples and fetches the
    recommendations according to the bought together algorithm. The fetched recommendations are in a list.
    Returns fetched products with the product id (dict) {product_id: [recommended_products]} {str: [str]}.
    """
    products = sample_support.load_samples(sample_type)
    result = {}
    for product in products:
        result[product] = bought_together.recommend_products(product, 4, sql_cursor)
    return result


def take_random_sampling():
    """
    Creates a validation set for the bought together algorithm with the random samples. Saves the set to
    random_validation_set.json.
    """
    sql_connection, sql_cursor = sql_c.connect()
    random_products = random_sampling(sql_cursor)
    convert_data.samples_product_dict(products=random_products,
                                      sql_cursor=sql_cursor,
                                      json_file=random_validation_file)
    sql_c.disconnect(sql_connection, sql_cursor)


def take_mandatory_sampling():
    """
    Creates a validation set for the bought together algorithm with the mandatory samples. Saves the set to
    mandatory_validation_set.json.
    """
    sql_connection, sql_cursor = sql_c.connect()
    random_products = random_sampling(sql_cursor, 'mandatory_samples')
    convert_data.samples_product_dict(products=random_products,
                                      sql_cursor=sql_cursor,
                                      json_file=mandatory_validation_file)
    sql_c.disconnect(sql_connection, sql_cursor)


if __name__ == '__main__':
    take_mandatory_sampling()
    take_random_sampling()
