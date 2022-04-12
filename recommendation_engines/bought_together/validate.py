import PostgreSQL.connect_postgresql_database as sql_c
import Validation.sample_support as sample_support
import Validation.data_conversion as convert_data
import recommend as bought_together
import json

json_validation_file = 'validation_set.json'


def random_sampling(sql_cursor, amount=50):
    products = sample_support.load_random_products(sql_cursor, amount)
    result = {}
    for product in products:
        result[product] = bought_together.recommend_products(product, 4, sql_cursor)
    return result


if __name__ == '__main__':
    con, cur = sql_c.connect()
    random_products = random_sampling(cur)
    convert_data.samples_product_dict(products=random_products,
                                      sql_cursor=cur,
                                      json_file=json_validation_file)
    sql_c.disconnect(con, cur)
