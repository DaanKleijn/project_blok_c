import PostgreSQL.connect_postgresql_database as sql_c
import Validation.sample_support as sample_support
import Validation.data_conversion as convert_data
import recommend as bought_together

json_validation_file = 'validation_set.json'


def sampling(sql_cursor):
    products = sample_support.load_random_products(sql_cursor, 50)
    result = {}
    for product in products:
        result[product] = bought_together.recommend(product, 4, sql_cursor)

    return result


def save_samples(sql_):
    """"""
    convert_data.get_validation_dict(products)
    result[product].append(convert_data.get_validation_dict(recommended_products, sql_cursor=sql_cursor))


if __name__ == '__main__':
    con, cur = sql_c.connect()
    sampling(cur)
