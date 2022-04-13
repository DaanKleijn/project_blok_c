# This file is dedicated to recommending products following the similar products algorithm.

import PostgreSQL.connect_postgresql_database as sql_c


def get_similars_query():
    """Returns an SQL query that fetches product ids of products similar to a given product."""
    return """SELECT similar_product__id FROM similars WHERE owner_product__id = %s"""


def get_similars_multiple_query(amount):
    """
    Takes a desired amount (int) as input. Returns an SQL query that fetches products, similar to a specified number of
    given products.
    """
    return """SELECT similar_product__id FROM similars 
    WHERE owner_product__id IN ({})""".format(','.join(['%s'] * amount))


def recommend_similars(product, sql_cursor):
    """
    Takes product(s) (list or str) and an SQL cursor as input. Fetches recommendations for someone interested in the
    specified product(s) and returns these recommendations.
    """
    if isinstance(product, str):
        query = get_similars_query()
        values = (product,)
    else:
        query = get_similars_multiple_query(len(product))
        values = tuple(product)

    sql_cursor.execute(query, values)

    return [product_id[0] for product_id in sql_cursor.fetchall()]


def recommending(amount, product):
    """
    Takes an amount (int) and the product id of a product (str) as input. Fetches recommendations for someone interested
    in the specified product. Returns the specified amount of recommendations.
    """
    sql_connection, sql_cursor = sql_c.connect()

    similar_products = recommend_similars(product, sql_cursor)
    sql_c.disconnect(sql_connection, sql_cursor)
    if amount >= len(similar_products):
        return similar_products[:amount]
    return similar_products


if __name__ == '__main__':
    print(recommending(4, '16862'))
