import PostgreSQL.connect_postgresql_database as sql_c
from datetime import timedelta


def traffic_all_time_query(amount_of_values):
    """Returns a query to fetch the product_id and the amount of times the product was bought during a given month."""
    # source: https://stackoverflow.com/questions/50334946/executemany-select-queries-with-psycopg2
    return """SELECT COUNT(ep.product__id), p.product__id 
    FROM event_products ep, sessions s, products p
    WHERE EXTRACT(MONTH FROM s.session_end) = %s
    AND ep.session__id = s.session__id 
    AND ep.product__id = p.product__id
    AND ep.product__id IN ({})
    AND ep.event_type = 'ordered'
    GROUP BY p.product__id;""".format(','.join(['%s'] * amount_of_values))


def traffic_day_query():
    """Returns all items that were bought with the amount of times it was bought since a given date."""
    return """SELECT COUNT(ep.product__id), p.product__id 
    FROM event_products ep, sessions s, products p
    WHERE ep.session__id = s.session__id 
    AND p.product__id = ep.product__id
    AND s.session_end >= %s
    AND ep.event_type = 'ordered'
    GROUP BY p.product__id;"""


def traffic_year_query(amount_of_values):
    """
    Returns a query to fetch the amount a product is bought and the product_id, ever since a given date, for all given
    products.
    """
    # source: https://stackoverflow.com/questions/50334946/executemany-select-queries-with-psycopg2
    return """SELECT COUNT(ep.product__id), p.product__id 
    FROM event_products ep, sessions s, products p 
    WHERE s.session_end >=  %s
    AND ep.session__id = s.session__id
    AND ep.product__id = p.product__id
    AND ep.event_type = 'ordered'
    AND ep.product__id IN ({})
    GROUP BY p.product__id;""".format(','.join(['%s'] * amount_of_values))


def get_all_traffic(products, months):
    """
    Takes a list with the month (list) [(str)] (['1', '2', '3'...]) and products (list) (str) as input.
    calculates the amount of times that product was looked at or bought for every month and puts these values in a
    dict with the product_id as key. Returns this dict.
    """
    sql_connection, sql_cursor = sql_c.connect()
    traffic_per_month = dict()
    traffic_query = traffic_all_time_query(len(products))

    for month in months:
        traffic_per_month[month] = dict()
        sql_cursor.execute(traffic_query, (month,) + tuple(products))
        product_count = sql_cursor.fetchall()
        for hits, product in product_count:
            traffic_per_month[month][product] = hits
    sql_c.disconnect(sql_connection, sql_cursor)

    return traffic_per_month


def get_daily_traffic(date, sql_cursor):
    """"""
    # Fetches all hits on products on the given date.
    # A hit means the product has been viewed or bought.
    # A product can receive one hit in one session.
    one_day_ago = date - timedelta(days=7)
    traffic_query = traffic_day_query()

    sql_cursor.execute(traffic_query, (one_day_ago,))
    frequency_products = dict()
    # Counts the amount of hits per product.
    for hit_count, product in sql_cursor.fetchall():
        frequency_products[str(product)] = hit_count

    return frequency_products


def get_yearly_traffic(products, sql_cursor, date):
    """
    Takes a list of product_id (str) as input.
    returns the amount of times that product was looked at or bought in that month (int).
    """
    minimum_date = date - timedelta(days=365)
    traffic_query = traffic_year_query(len(products))
    sql_cursor.execute(traffic_query, (minimum_date,) + tuple(products))
    products = sql_cursor.fetchall()

    return products


def get_daily_bar(total_traffic):
    """
    Takes a list with 12 count values. Each value represents the amount of hits a given product has ever received in
    a month.
    Calculates the minimum amount of hits a product has to receive any given month for that month to receive signi
    """
    average_traffic = total_traffic / 52
    return (average_traffic * 1.4) + 50


def get_bar_product(traffic_per_month):
    """
    Takes a list with 12 count values. Each value represents the amount of hits a given product has ever received in
    a month.
    Calculates the minimum amount of hits a product has to receive any given month for that month to receive signi
    """
    average_traffic = sum(traffic_per_month) / 12
    return average_traffic * 1.4 + 50
