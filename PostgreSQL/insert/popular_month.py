# a file dedicated to creating and inserting values into the popular_month column in the database's products table.

import psycopg2.extras


def create_popular_column_query():
    """Returns an SQL query that creates the popular_month column in the database's products table."""
    return """ALTER TABLE products
    ADD popular_month VARCHAR;"""


def create_column_popular_months(sql_connection, sql_cursor):
    """Takes an SQL connection and cursor as input. Adds the 'popular_month' column to the products table."""
    sql_query = create_popular_column_query()
    sql_cursor.execute(sql_query)
    sql_connection.commit()


def update_popular_month_query():
    """
    Returns an SQL query that updates the 'popular_month' in the products table of a given product_id. It takes two
    values, the value you want to set and a product_id.
    """
    return """UPDATE products
    SET popular_month = %s
    WHERE product__id = %s"""


def update_popular_month(sql_cursor, popular_months):
    """
    Takes an SQL query and a list containing tuples that contain two values, popular_month and product__id, (list)
    [(str, str)] as input.
    Writes these values to the popular_month column in the database's products table.
    """
    update_pop_month = update_popular_month_query()
    psycopg2.extras.execute_batch(sql_cursor, update_pop_month, popular_months)
