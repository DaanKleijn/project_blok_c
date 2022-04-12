from datetime import datetime
import PostgreSQL.connect_postgresql_database as sql_c
import PostgreSQL.load.traffic.load_traffic as traffic


def get_daily_bar(total_traffic):
    """
    Takes a list with 12 count values. Each value represents the amount of hits a given product has ever received in
    a month.
    Calculates the minimum amount of hits a product has to receive any given week for that traffic to be significantly
    higher. (140 % + 50)
    """
    average_traffic = total_traffic / 52
    return (average_traffic * 1.4) + 50


def products_trending(amount, sql_cursor):
    """
    Takes the desired amount of recommendations (int) as input. Calculates which products get significantly more traffic
    than usual.
    Traffic is measured by the amount of unique orders and is measured over the last week. The product is trending if
    the measured traffic is 40 % + 50 higher than the average traffic over the last year.
    Returns the desired amount of trending products (list).
    """
    date = datetime.today()
    trending = list()
    frequency_products = traffic.get_daily_traffic(date, sql_cursor)
    # Cycles through all products with their hit_count
    total_traffic = traffic.get_yearly_traffic(list(frequency_products.keys()), date, sql_cursor)

    for total_hit_count, product in total_traffic:
        product_bar = get_daily_bar(total_hit_count)
        # If the amount of hits * 30 (so we can compare it to data over a month instead of over a day) is greater than
        # (average hits per month * 1.4 + 50), the product is trending.
        if frequency_products[product] >= product_bar:
            trending.append(product)
    if len(trending) >= amount:
        return trending[:amount]

    return trending


if __name__ == '__main__':
    con, cur = sql_c.connect()
    print(products_trending(4, cur))
    sql_c.disconnect(con, cur)
