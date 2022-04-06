import PostgreSQL.connect_postgresql_database as sql_c
import load_data_sql as sql_l


def create_column_popular_months(sql_connection, sql_cursor):
    sql_query = """ALTER TABLE products
ADD popular_month VARCHAR;"""
    sql_cursor.execute(sql_query)
    sql_connection.commit()


def update_popular_month_query():
    return """UPDATE products AS p
    SET popular_months = new.popular_month
    FROM (VALUES %s)
    AS new(popular_month, product__id)
    WHERE product__id = new.product__id"""


def product_traffic_query():
    return """SELECT ep.product__id FROM event_products ep, sessions s 
    WHERE EXTRACT(MONTH FROM s.session_end) = %s 
    and ep.session__id = s.session__id 
    and ep.product__id = %s;"""


def product_traffic_month(month, product_id):
    """"""
    sql_connection, sql_cursor = sql_c.connect()
    sql_query = product_traffic_query()
    sql_cursor.execute(sql_query, (month, product_id))
    products = sql_cursor.fetchall()

    return len(products)


def get_popular_months(traffic_per_month):
    """"""
    average_traffic = sum(traffic_per_month) / 12
    bar = average_traffic * 1.4 + 50
    popular_months = ''
    for traffic_month in traffic_per_month:
        if traffic_month >= bar:
            # gets the month by finding the index of the traffic and adding one, as the traffic of month 1 is indexed on
            # index 0 and so on.
            popular_month = str(traffic_per_month.index(traffic_month) + 1)
            popular_months += ', {}'.format(popular_month)
    if popular_months:
        return popular_months[2:]


def calculate_popular_months_products():
    """"""
    sql_connection, sql_cursor = sql_c.connect()
    products_query = sql_l.all_product_ids_query()
    sql_cursor.execute(products_query)
    months = [str(i) for i in range(1, 13)]
    product_popular_month = tuple()
    for product in [product_id[0] for product_id in sql_cursor.fetchall()]:
        traffic_per_month = list()
        for month in months:
            traffic = product_traffic_month(month=month, product_id=product)
            traffic_per_month.append(traffic)

        popular_months = get_popular_months(traffic_per_month)
        product_popular_month += ((popular_months, product),)
        print(product, popular_months)
    update_pop_month = update_popular_month_query()
    sql_cursor.execute(update_pop_month, product_popular_month)
    sql_connection.commit()


if __name__ == '__main__':
    calculate_popular_months_products()
