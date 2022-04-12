import recommendation_engines.similar_products.recommend as similar_products
import Validation.sample_support as sample_support
import Validation.data_conversion as convert_data
import PostgreSQL.connect_postgresql_database as sql_c

random_validation_file = 'random_validation_set.json'
mandatory_validation_file = 'mandatory_validation_set.json'


def random_sampling(sql_cursor, sample_type='random_samples'):
    """"""
    random_products = sample_support.load_samples(sample_type)
    product_data = dict()
    for product in random_products:
        product_data[product] = similar_products.recommend_similars(product=product,
                                                                    sql_cursor=sql_cursor)
    return product_data


def take_random_sampling():
    sql_connection, sql_cursor = sql_c.connect()
    data_dict = random_sampling(sql_cursor)
    convert_data.samples_product_dict(sql_cursor=sql_cursor,
                                      products=data_dict,
                                      json_file=random_validation_file)


def take_mandatory_sampling():
    sql_connection, sql_cursor = sql_c.connect()
    data_dict = random_sampling(sql_cursor, 'mandatory_samples')
    convert_data.samples_product_dict(sql_cursor=sql_cursor,
                                      products=data_dict,
                                      json_file=mandatory_validation_file)


if __name__ == '__main__':
    take_random_sampling()
    take_mandatory_sampling()
