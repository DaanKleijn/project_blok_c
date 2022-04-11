import PostgreSQL.load.traffic.traffic_queries as traffic_queries
from datetime import timedelta


def get_all_traffic_per_month(products, months, sql_cursor):
    """
    Takes a list with the month (list) [(str)] (['1', '2', '3'...]) and products (list) (str) as input.
    calculates the amount of times that product was bought for every month and puts these values in a
    dict with the product_id as key. Returns this dict.
    """
    traffic_per_month = dict()
    print(products)
    traffic_query = traffic_queries.traffic_all_time_formatted_query(len(products))

    for month in months:
        traffic_per_month[month] = dict()
        sql_cursor.execute(traffic_query, (month,) + tuple(products))
        product_count = sql_cursor.fetchall()
        for hits, product in product_count:
            traffic_per_month[month][product] = hits

    return traffic_per_month


def get_daily_traffic(date, sql_cursor):
    """
    Takes the current date (datetime) and a list of products (list) (str) as input.
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
    Takes a list of product_id (str) as input.
    Returns the amount of times that product was bought that year. (int).
    """
    minimum_date = date - timedelta(days=365)
    traffic_query = traffic_queries.traffic_year_formatted_query(len(products))
    sql_cursor.execute(traffic_query, (minimum_date,) + tuple(products))
    products = sql_cursor.fetchall()

    return products
