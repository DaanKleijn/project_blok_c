import recommend as similar_products
import Validation.sample_support as sample_support
import Validation.data_conversion as convert_data
import PostgreSQL.connect_postgresql_database as sql_c

json_validation_file = 'similar_validation_set.json'


def random_sampling(sql_cursor):
    """"""
    random_products = sample_support.load_random_products(sql_cursor)
    product_data = dict()
    for product in random_products:
        product_data[product] = similar_products.recommend_similars(product=product,
                                                                    sql_cursor=sql_cursor)
    return product_data


if __name__ == '__main__':
    sql_connection, sql_cursor = sql_c.connect()
    data_dict = random_sampling(sql_cursor)
    convert_data.samples_product_dict(sql_cursor=sql_cursor,
                                      products=data_dict,
                                      json_file=json_validation_file)
