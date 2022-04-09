import PostgreSQL.connect_postgresql_database as sql_c


def product_traffic_query():
    """returns a query to return the product_id for everytime that product is looked at in a certain month."""
    return """SELECT ep.product__id FROM event_products ep, sessions s 
    WHERE EXTRACT(MONTH FROM s.session_end) = %s
    AND EXTRACT(YEAR FROM s.session_end) =  %s
    AND ep.session__id = s.session__id 
    AND ep.product__id = %s;"""


def get_traffic_one_month(month, product_id, year='2022'):
    """
    Takes a month (str) represented as a number (eg. '1' for januari) and a product_id (str) as input.
    returns the amount of times that product was looked at or bought in that month (int).
    """
    sql_connection, sql_cursor = sql_c.connect()
    sql_query = product_traffic_query()
    sql_cursor.execute(sql_query, (month, year, product_id))
    products = sql_cursor.fetchall()

    return len(products)


def get_traffic_all_months(product, months):
    """
    Takes a list with the month (list) [(str)] (['1', '2', '3'...]) and a product_id (str) as input.
    calculates the amount of times that product was looked at or bought for every month and puts these values in a list.
    returns this list (list) [int]
    """
    traffic_per_month = list()
    for month in months:
        traffic = get_traffic_one_month(month=month, product_id=product)
        traffic_per_month.append(traffic)

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
