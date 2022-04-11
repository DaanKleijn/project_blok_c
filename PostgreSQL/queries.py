def all_product_ids_query():
    return """SELECT product__id FROM products"""


def profile_id_buid_query():
    """"""
    return """SELECT profile__id FROM buids WHERE buid = '{}'"""


def product_traffic_month(month):
    """"""
    return """SELECT ep.product__id FROM event_products ep, sessions s 
    WHERE EXTRACT(MONTH FROM s.session_end) = %s and ep.session__id = s.session__id;"""


def products_trending(date):
    """"""
    return """SELECT product__id FROM event_products ep, sessions s 
    WHERE ep.session__id = s.session__id AND CAST(s.session_end AS DATE) = %s"""


def product_gender():
    sql = f'SELECT product__id FROM products WHERE gender = (SELECT gender FROM products WHERE product__id = %s) AND ' \
          f'product__id != %s;'
    return sql


def product_price():
    sql = f'SELECT selling_price FROM products WHERE selling_price = (SELECT selling_price FROM products WHERE ' \
          f'product__id = %s) AND product__id != %s;'
    return sql


def product_category(category_type='sub_category'):
    """"""
    return """SELECT product__id FROM products WHERE {} = %s""".format(category_type)


def event_product_query():
    """"""
    return """SELECT ep.product__id FROM event_products ep, sessions s, products p 
    WHERE ep.session__id = s.session__id 
    AND ep.product__id = p.product__id
    AND s.session__id in (SELECT session__id FROM event_products WHERE product__id = %s)
    AND ep.event_type = %s
    AND ep.product__id != %s;"""
