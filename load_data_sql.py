import PostgreSQL.connect_postgresql_database as sql_c


def profile_id_buid_query():
    """"""
    return """SELECT profile__id FROM buids WHERE buid = '{}'"""


def product_traffic_month(month):
    """"""
    sql_query = """SELECT ep.product__id FROM event_products ep, sessions s 
    WHERE EXTRACT(MONTH FROM s.session_end) = %s and ep.session__id = s.session__id;"""


def products_trending(date):
    """"""
    sql_query = """SELECT product__id FROM event_products ep, sessions s 
    WHERE ep.session__id = s.session__id AND CAST(s.session_end AS DATE) = %s"""


def product_gender():
    product_query = f'SELECT product_id FROM products'
    gender_query = f'SELECT gender FROM products'
    return product_query, gender_query