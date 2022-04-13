# This file is dedicated to creating datasets used to validate the similar products algorithm.

import recommendation_engines.similar_products.recommend as similar_products
import Validation.sample_support as sample_support
import Validation.data_conversion as convert_data
import PostgreSQL.connect_postgresql_database as sql_c

random_validation_file = 'random_validation_set.json'
mandatory_validation_file = 'mandatory_validation_set.json'


def random_sampling(sql_cursor, sample_type='random_samples'):
    """
    Takes an SQL cursor and optionally a sample type (str) as input. Loads the specified type of samples and fetches the
    recommendations according to the similar products algorithm. The fetched recommendations are in a list.
    Returns fetched products with the product id (dict) {product_id: [recommended_products]} {str: [str]}.
    """
    random_products = sample_support.load_samples(sample_type)
    product_data = dict()
    for product in random_products:
        product_data[product] = similar_products.recommend_similars(product=product,
                                                                    sql_cursor=sql_cursor)
    return product_data


def take_random_sampling():
    """
    Creates a validation set for the similar product algorithm with the random samples. Saves the set to
    random_validation_set.json.
    """
    sql_connection, sql_cursor = sql_c.connect()
    data_dict = random_sampling(sql_cursor)
    convert_data.samples_product_dict(sql_cursor=sql_cursor,
                                      products=data_dict,
                                      json_file=random_validation_file)


def take_mandatory_sampling():
    """
    Creates a validation set for the similar product algorithm with the mandatory samples. Saves the set to
    mandatory_validation_set.json.
    """
    sql_connection, sql_cursor = sql_c.connect()
    data_dict = random_sampling(sql_cursor, 'mandatory_samples')
    convert_data.samples_product_dict(sql_cursor=sql_cursor,
                                      products=data_dict,
                                      json_file=mandatory_validation_file)


if __name__ == '__main__':
    take_random_sampling()
    take_mandatory_sampling()
