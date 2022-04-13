# This file is dedicated to recommending products following the date filtering algorithm.

from datetime import datetime
import PostgreSQL.load.products.load_products as load_products
import PostgreSQL.connect_postgresql_database as sql_c


def recommended_products(product_amount, sql_cursor):
    """
    Takes the amount of desired products (int) as input.
    Fetches products that are more popular during the current month than in other months.
    A more popular month gets 40 % + 50 more sales than an average month.
    Returns the desired amount of products (list) [str].
    """
    # fetches current month
    month = str(int(datetime.today().strftime('%m')))
    trending_products = load_products.date_filtered(month, sql_cursor)
    if len(trending_products) >= product_amount:
        return trending_products[:product_amount]
    return trending_products


def recommended_products_month(month, product_amount, sql_cursor):
    """
    Takes the amount of desired products (int) as input.
    Fetches products that are more popular during the current month than in other months.
    A more popular month gets 40 % + 50 more sales than an average month.
    Returns the desired amount of products (list) [str].
    """
    trending_products = load_products.date_filtered(month, sql_cursor)

    if len(trending_products) >= product_amount:
        return trending_products[:product_amount]
    return trending_products


def recommending(product_amount):
    """
    Takes a desired product_amount (int) as input. Fetches the specified amount of recommendations according to the
    date filtering algorithm and returns them.
    """
    sql_connection, sql_cursor = sql_c.connect()
    recommended_prods = recommended_products(product_amount, sql_cursor)
    sql_c.disconnect(sql_connection, sql_cursor)

    return recommended_prods


if __name__ == '__main__':
    con, cur = sql_c.connect()
    print(recommended_products(100, cur))
    sql_c.disconnect(con, cur)
