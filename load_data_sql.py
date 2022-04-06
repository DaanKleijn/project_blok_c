import PostgreSQL.connect_postgresql_database as sql_c


def all_product_ids_query():
    return """SELECT product__id FROM products"""


def profile_id_buid_query():
    """"""
    return """SELECT profile__id FROM buids WHERE buid = '{}'"""
