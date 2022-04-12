import PostgreSQL.connect_postgresql_database as sql_c


def get_similars_query():
    """"""
    return """SELECT similar_product__id FROM similars WHERE owner_product__id = %s"""


def get_similars_multiple_query(amount_of_values):
    """"""
    return """SELECT similar_product__id FROM similars 
    WHERE owner_product__id IN ({})""".format(','.join(['%s'] * amount_of_values))


def recommend_similars(product, sql_cursor):
    """"""
    if isinstance(product, str):
        query = get_similars_query()
        values = (product,)
    else:
        query = get_similars_multiple_query(len(product))
        values = tuple(product)

    sql_cursor.execute(query, values)

    return [product_id[0] for product_id in sql_cursor.fetchall()]


def recommending(amount, product):
    """"""
    sql_connection, sql_cursor = sql_c.connect()

    similar_products = recommend_similars(product, sql_cursor)
    sql_c.disconnect(sql_connection, sql_cursor)
    if amount >= len(similar_products):
        return similar_products[:amount]
    return similar_products


