import PostgreSQL.connect_postgresql_database as sql_c
import recommendation_engines.statistics as stats
import PostgreSQL.load.products.load_products as sql_load


def recommend(product_id, product_amount):
    """
    Takes a product_id (str) and an amount (int) as input.
    Returns the given amount of product_ids of all products ordered together with the input product (list) [str].
    """
    sql_connection, sql_cursor = sql_c.connect()
    products_ordered_together = sql_load.ordered_together_with(product_id, sql_cursor)
    frequency_products = stats.get_frequency(products_ordered_together)
    recommended_products = stats.highest_counts(frequency_products, product_amount)
    sql_c.disconnect(sql_connection, sql_cursor)
    return recommended_products


if __name__ == '__main__':
    con, cur = sql_c.connect()
    print(recommend('40773', 4))

