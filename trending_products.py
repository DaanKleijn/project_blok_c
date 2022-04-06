import PostgreSQL.connect_postgresql_database as sql_c
import traffic_over_products as traffic


def products_trending(date):
    """"""
    trending = list()
    sql_connection, sql_cursor = sql_c.connect()
    sql_query = """SELECT product__id FROM event_products ep, sessions s 
    WHERE ep.session__id = s.session__id AND CAST(s.session_end AS DATE) = %s"""
    sql_cursor.execute(sql_query, (date,))
    frequency_products = {}
    for product in [product[0] for product in sql_cursor.fetchall()]:
        try:
            frequency_products[product] += 1
        except KeyError:
            frequency_products[product] = 1
    months = [str(i) for i in range(1, 13)]
    for product, frequency in list(frequency_products.items()):
        traffic_per_month = traffic.get_traffic_all_months(product, months)
        product_bar = traffic.get_bar_product(traffic_per_month)
        if (frequency * 30) >= product_bar:
            trending.append(product)

    return trending
