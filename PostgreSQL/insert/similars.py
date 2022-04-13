# a file dedicated to creating and inserting values into the similars table in the SQL database.


import psycopg2.extras


def insert_similar_query():
    """
    Returns an SQL query that will insert two values, owner__product_id and similar_product__id, into the similars
    table. Format order is owner__product_id, similar_product__id.
    """
    return """INSERT INTO similars
    VALUES (%s, %s)"""


def upload_similar(sql_cursor, similar_values):
    """
    Takes an SQL cursor and two product_ids, one original product (str) and one similar product (str), as input.
    Uploads these values to the similars table in the database. Doesn't return anything.
    """
    similar_update_query = insert_similar_query()
    psycopg2.extras.execute_batch(sql_cursor, similar_update_query, similar_values, page_size=10000)
