import PostgreSQL.connect_postgresql_database as sql_c
import recommendation_engines.statistics as stats
import PostgreSQL.load.products.load_products as sql_load


def recommend(product_id, product_amount, sql_cursor):
    """
    Takes a product_id (str) and an amount (int) as input.
    Returns the given amount of product_ids of all products ordered together with the input product (list) [str].
    """
    products_ordered_together = sql_load.ordered_together_with(product_id, sql_cursor)
    frequency_products = stats.get_frequency(products_ordered_together)
    recommended_products = stats.highest_counts(frequency_products, product_amount)

    return recommended_products


if __name__ == '__main__':
    con, cur = sql_c.connect()
    print(recommend('40773', 4, cur))
    sql_c.disconnect(con, cur)