import PostgreSQL.connect_postgresql_database as sql_c


def product_traffic_all_time_query(amount_of_values):
    """returns a query to return the product_id for everytime that product is looked at in a certain month."""
    return """SELECT COUNT(ep.product__id), p.product__id FROM event_products ep, sessions s, products p
    WHERE EXTRACT(MONTH FROM s.session_end) = %s
    AND ep.session__id = s.session__id 
    AND ep.product__id = p.product__id
    AND ep.product__id IN ({})
    AND ep.event_type = 'ordered'
    GROUP BY p.product__id;""".format(','.join(['%s'] * amount_of_values))


def get_all_traffic(products, months):
    """
    Takes a list with the month (list) [(str)] (['1', '2', '3'...]) and a product_id (str) as input.
    calculates the amount of times that product was looked at or bought for every month and puts these values in a list.
    returns this list (list) [int]
    """
    sql_connection, sql_cursor = sql_c.connect()
    traffic_per_month = dict()
    traffic_query = product_traffic_all_time_query(len(products))

    for month in months:
        traffic_per_month[month] = dict()
        values = (month,) + products
        sql_cursor.execute(traffic_query, values)
        product_count = sql_cursor.fetchall()
        for hits, product in product_count:
            traffic_per_month[month][product] = hits
    sql_c.disconnect(sql_connection, sql_cursor)

    return traffic_per_month
