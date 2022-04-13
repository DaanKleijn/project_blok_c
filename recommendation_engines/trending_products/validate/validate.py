# This file is dedicated to creating a dataset used to validate the trending algorithm.

import Validation.date_helper as date_helper
import Validation.data_conversion as convert_data
import PostgreSQL.connect_postgresql_database as sql_c
import recommendation_engines.trending_products.recommend as trending

random_validation_file = 'random_validation_set.json'


def random_sampling(sql_cursor, amount=10):
    """
    Takes an SQL cursor and optionally an amount (str) as input. Chooses the desired amount of random dates between
    2017-12-1 2018-12-31. Fetches the recommendations according to the trending algorithm.
    The fetched recommendations are in a list.
    Returns fetched products with the product id (dict) {date: [recommended_products]} or {str: [str]}.
    """
    random_dates = date_helper.get_random_dates('2017-12-1', '2018-12-31', amount)
    product_data = {}
    for random_date in random_dates:
        product_data[random_date.strftime('%Y-%m-%d')] = trending.products_trending_date(amount=20,
                                                                                         date=random_date,
                                                                                         sql_cursor=sql_cursor)
    return product_data


def take_random_sampling():
    """
    Creates a validation set for the trending algorithm with the 10 random sample dates. Saves the set to
    random_validation_set.json.
    """
    sql_connection, sql_cursor = sql_c.connect()
    product_data = random_sampling(sql_cursor)
    convert_data.samples_other_dict(products=product_data,
                                    sql_cursor=sql_cursor,
                                    json_file=random_validation_file)


if __name__ == '__main__':
    take_random_sampling()
