import PostgreSQL.connect_postgresql_database as sql_c
import recommendation_engines.statistics as stats
import PostgreSQL.queries as sql_queries


def get_all_ordered_together(product):
    """"""
    sql_connection, sql_cursor = sql_c.connect()
    products_query = sql_queries.event_product_query()
    sql_cursor.execute(products_query, (product, 'ordered', product))
    return [ordered_product[0] for ordered_product in sql_cursor.fetchall()]


def recommend(product_id, amount):
    """"""
    products_ordered_together = get_all_ordered_together(product_id)
    frequency_products = stats.get_frequency(products_ordered_together)
    recommended_products = stats.highest_counts(frequency_products, amount)
    return recommended_products


if __name__ == '__main__':
    print(recommend('40773', 4))
