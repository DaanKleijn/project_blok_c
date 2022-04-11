def create_column_popular_months(sql_connection, sql_cursor):
    """Returns a query that adds the column 'popular_month' to the products table."""
    sql_query = """ALTER TABLE products
    ADD popular_month VARCHAR;"""
    sql_cursor.execute(sql_query)
    sql_connection.commit()


def update_popular_month_query():
    """
    Returns a query that updates 'popular_month' of a given product_id to a given value.
    Format order is month_value, product_id.
    """
    return """UPDATE products
    SET popular_month = %s
    WHERE product__id = %s"""
