# This file is dedicated to fetching data about product traffic (views or sales) from the SQL database.

import PostgreSQL.load.traffic.traffic_queries as traffic_queries
from datetime import timedelta


def get_all_traffic_per_month(products, months, sql_cursor):
    """
    Takes a list with the months (list) [str] (months represented by integers ['1', '2', '3'...]), products (list)
    [str] and an SQL cursor as input.
    Counts the amount of times that product was bought per month and puts these values in a dict.
    Returns this dict (dict) {month: {product_id : month_count}}.

    This might seem like a really convoluted way to record the counts. Why not just use a list?
    Not all product are sold in every month. When there is no sale, there will be no count for the database to return.
    The product_id will also not be returned. So not all list would result in 12 items. For incomplete lists, it will
    be impossible to tell with certainty which months the index refer to. It is a hassle to deal with this incomplete
    data at this point, so we save it to a dict like this and deal with it later.
    """
    traffic_per_month = dict()
    traffic_query = traffic_queries.traffic_all_time_formatted_query(len(products))

    for month in months:
        traffic_per_month[month] = dict()
        sql_cursor.execute(traffic_query, (month,) + tuple(products))
        # fetches amount of sales this month (ever), together with the product id.
        product_count = sql_cursor.fetchall()
        # records the amount of hits for the product this month.
        for hits, product in product_count:
            traffic_per_month[month][product] = hits

    return traffic_per_month


def get_daily_traffic(date, sql_cursor):
    """
    Takes the current date (datetime) and an SQL cursor as input.
    Returns all products that were bought over the last seven days, together with the amount of times they were bought
    (dict) {product: count}.
    """
    # Fetches all hits on products on the given date.
    # A hit means the product has been viewed or bought.
    # A product can receive one hit in one sessions.
    one_day_ago = date - timedelta(days=7)
    traffic_query = traffic_queries.traffic_day_query()

    sql_cursor.execute(traffic_query, (one_day_ago,))
    frequency_products = dict()
    # Counts the amount of hits per product.
    for hit_count, product in sql_cursor.fetchall():
        frequency_products[str(product)] = hit_count

    return frequency_products


def get_yearly_traffic(products, date, sql_cursor):
    """
    Takes a list of product_id (str), the current date (datetime) and an SQL cursor as input.
    Returns the amount of times that product was bought in the last year. (int).
    """
    minimum_date = date - timedelta(days=365)
    traffic_query = traffic_queries.traffic_year_formatted_query(len(products))
    sql_cursor.execute(traffic_query, (minimum_date,) + tuple(products))
    products = sql_cursor.fetchall()

    return products
