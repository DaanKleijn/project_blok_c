import time
from datetime import datetime
import PostgreSQL.connect_postgresql_database as sql_c
import recommendation_engines.product_traffic as traffic
import recommendation_engines.statistics as stats


def products_trending(date):
    """"""
    start_time = time.time_ns()
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
        print(product_bar, frequency_products[product], product)
        if frequency_products[product] >= product_bar:
            trending.append(product)

    return trending, '{:.4f} secondes'.format((time.time_ns() - start_time) / 1000000000)


current_time = datetime.today()
current_time = datetime(2018, 6, 15, 10)
print(products_trending(current_time))
