import PostgreSQL.connect_postgresql_database as sql_c


def all_product_ids_query():
    return """SELECT product__id FROM products"""


def profile_id_buid_query():
    """"""
    return """SELECT profile__id FROM buids WHERE buid = '{}'"""


def product_gender():
    sql = f'SELECT product__id FROM products WHERE gender = (SELECT gender FROM products WHERE product__id = %s) AND ' \
          f'product__id != %s;'
    return sql


def product_price():
    sql = f'SELECT product__id FROM products WHERE selling_price = (SELECT selling_price FROM products WHERE ' \
          f'product__id = %s) AND product__id != %s;'
    return sql


def product_category(category_type='sub_category'):
    """"""
    return """SELECT product__id FROM products WHERE {} = %s""".format(category_type)
