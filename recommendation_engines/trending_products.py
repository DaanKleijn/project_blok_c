import PostgreSQL.connect_postgresql_database as sql_c
from recommendation_engines import product_traffic as traffic


def products_trending(date):
    """"""
    trending = list()
    # Connects to the database
    sql_connection, sql_cursor = sql_c.connect()
    sql_query = """SELECT product__id FROM event_products ep, sessions s 
    WHERE ep.session__id = s.session__id AND CAST(s.session_end AS DATE) = %s"""
    # Fetches all hits on products on the given date.
    # A hit means the product has been viewed or bought.
    # A product can receive one hit in one session.
    sql_cursor.execute(sql_query, (date,))
    frequency_products = {}
    # Counts the amount of hits per product.
    for product in [product[0] for product in sql_cursor.fetchall()]:
        try:
            frequency_products[product] += 1
        except KeyError:
            frequency_products[product] = 1
    months = [str(i) for i in range(1, 13)]
    # Cycles through all products with their hit_count
    for product, hit_count in list(frequency_products.items()):
        traffic_per_month = traffic.get_traffic_all_months(product, months)
        product_bar = traffic.get_bar_product(traffic_per_month)
        # If the amount of hits * 30 (so we can compare it to data over a month instead of over a day) is greater than
        # (average hits per month * 1.4 + 50), the product is trending.
        if (hit_count * 30) >= product_bar:
            trending.append(product)

    return trending


print(products_trending('2017-10-12'))
