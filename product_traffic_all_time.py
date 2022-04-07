import PostgreSQL.connect_postgresql_database as sql_c


# amount of product traffic over a given month.
def product_traffic_all_time_query():
    """returns a query to return the product_id for everytime that product is looked at in a certain month."""
    return """SELECT COUNT(ep.product__id) FROM event_products ep, sessions s 
    WHERE EXTRACT(MONTH FROM s.session_end) = %s 
    AND ep.session__id = s.session__id 
    AND ep.product__id = %s;"""


def get_traffic_one_month_all_time(month, product_id, sql_cursor):
    """
    Takes a month (str) represented as a number (eg. '1' for januari) and a product_id (str) as input.
    returns the amount of times that product was looked at or bought in that month (int).
    """
    traffic_query = product_traffic_all_time_query()
    sql_cursor.execute(traffic_query, (month, product_id))
    product_count = sql_cursor.fetchone()

    return product_count[0]


def get_traffic_all_months_all_time(product, months):
    """
    Takes a list with the month (list) [(str)] (['1', '2', '3'...]) and a product_id (str) as input.
    calculates the amount of times that product was looked at or bought for every month and puts these values in a list.
    returns this list (list) [int]
    """
    sql_connection, sql_cursor = sql_c.connect()
    traffic_per_month = list()
    traffic_query = product_traffic_all_time_query()

    for month in months:
        sql_cursor.execute(traffic_query, (month, product))
        product_count = sql_cursor.fetchone()
        traffic_per_month.append(product_count[0])
    sql_c.disconnect(sql_connection, sql_cursor)

    return traffic_per_month


# minimum activity for given product to be significant.
def get_bar_product(traffic_per_month):
    """
    Takes a list with 12 count values. Each value represents the amount of hits a given product has ever received in
    a month.
    Calculates the minimum amount of hits a product has to receive any given month for that month to receive signi
    """
    average_traffic = sum(traffic_per_month) / 12
    return average_traffic * 1.4 + 50
