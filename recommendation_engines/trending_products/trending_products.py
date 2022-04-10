from datetime import datetime
import PostgreSQL.connect_postgresql_database as sql_c
import recommendation_engines.product_traffic as traffic


def products_trending(amount):
    """
    Takes the desired amount of recommendations (int) as input. Calculates which products get significantly more traffic
    than usual.
    Traffic is measured by the amount of unique orders and is measured over the last week. If the amount of traffic over
    the last week was more than the (average traffic over the last year * 1.4) + 50, the product will be marked as
    trending.
    Returns the desired amount of trending products (list).
    """
    date = datetime.today()
    trending = list()
    # Connects to the database
    sql_connection, sql_cursor = sql_c.connect()
    frequency_products = traffic.get_daily_traffic(date, sql_cursor)
    # Cycles through all products with their hit_count
    total_traffic = traffic.get_yearly_traffic(list(frequency_products.keys()), sql_cursor, date)

    for total_hit_count, product in total_traffic:
        product_bar = traffic.get_daily_bar(total_hit_count)
        # If the amount of hits * 30 (so we can compare it to data over a month instead of over a day) is greater than
        # (average hits per month * 1.4 + 50), the product is trending.
        if frequency_products[product] >= product_bar:
            trending.append(product)

    if len(trending) >= amount:
        return trending[:amount]

    return trending
