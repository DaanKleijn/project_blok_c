# This file is dedicated to recommending products following the bought together algorithm.

import PostgreSQL.connect_postgresql_database as sql_c
import recommendation_engines.frequencies as stats
import PostgreSQL.load.products.load_products as sql_load


def recommend_products(product_id, product_amount, sql_cursor):
    """
    Takes a product_id (str) and an amount (int) as input.
    Returns the given amount of product_ids of all products ordered together with the input product (list) [str].
    """
    products_ordered_together = sql_load.ordered_together_with(product_id, sql_cursor)
    frequency_products = stats.get_frequency(products_ordered_together)
    recommended_prods = stats.highest_counts(frequency_products, product_amount)

    return recommended_prods


def recommending(product_id, product_amount):
    """
    Takes a product id (str) and a product_amount (int) as input. Connects to the SQL database. Fetches products
    that, in a previous session, have been bought together with the input product and find which products have been
    bought together most with this product.
    Returns the specified amount of products that have been bought together with the input product the most often
    (list) [str].
    """
    sql_connection, sql_cursor = sql_c.connect()
    recommended_prods = recommend_products(product_id, product_amount, sql_cursor)
    sql_c.disconnect(sql_connection, sql_cursor)
    return recommended_prods


if __name__ == '__main__':
    con, cur = sql_c.connect()
    print(recommend_products('40773', 4, cur))
    sql_c.disconnect(con, cur)
