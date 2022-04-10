import time
from datetime import datetime
import PostgreSQL.connect_postgresql_database as sql_c


def product_pop_month_query():
    """Returns a query that fetches all product_ids of products that are more popular in a given month."""
    return """SELECT product__id FROM products WHERE popular_month= %s"""


def recommend(product_amount):
    """
    Takes the amount of desired products (int) as input.
    Fetches products that are more popular during the current month than in other months.
    A more popular month gets 40 % + 50 more sales than an average month.
    Returns the desired amount of products (list) [str].
    """
    month = str(int(datetime.today().strftime('%m')))
    start_time = time.time_ns()
    sql_connection, sql_cursor = sql_c.connect()
    product_query = product_pop_month_query()
    sql_cursor.execute(product_query, (month,))

    trending_products = [product[0] for product in sql_cursor.fetchall()], '{:.4f} secondes'.format(
        (time.time_ns() - start_time) / 1000000000)
    if len(trending_products) >= product_amount:
        return trending_products[:product_amount]
    return trending_products


if __name__ == '__main__':
    print(recommend(4))
