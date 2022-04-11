import psycopg2.extras


def insert_similar_query():
    return """INSERT INTO similars
    VALUES (%s, %s)"""


def upload_similar(sql_cursor, similar_values):
    """"""
    similar_update_query = insert_similar_query()
    psycopg2.extras.execute_batch(sql_cursor, similar_update_query, similar_values, page_size=10000)
