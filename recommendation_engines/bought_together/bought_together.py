import PostgreSQL.connect_postgresql_database as sql_c
import recommendation_engines.statistics as stats
import PostgreSQL.queries as sql_queries


def get_all_ordered_together(product):
    """
    Takes a product_id as input. Fetches the product_id of all products ordered together with the input product.
    Returns all fetched products (list) [str].
    """
    sql_connection, sql_cursor = sql_c.connect()
    products_query = sql_queries.event_product_query()
    sql_cursor.execute(products_query, (product, 'ordered', product))
    return [ordered_product[0] for ordered_product in sql_cursor.fetchall()]


def recommend(product_id, product_amount):
    """
    Takes a product_id (str) and an amount (int) as input.
    Returns the given amount of product_ids of all products ordered together with the input product (list) [str].
    """
    products_ordered_together = get_all_ordered_together(product_id)
    frequency_products = stats.get_frequency(products_ordered_together)
    recommended_products = stats.highest_counts(frequency_products, product_amount)
    return recommended_products


if __name__ == '__main__':
    print(recommend('40773', 4))
