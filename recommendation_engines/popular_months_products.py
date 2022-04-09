import PostgreSQL.connect_postgresql_database as sql_c
from PostgreSQL import load_data_sql as sql_l
import product_traffic_all_time as traffic
# TODO: account for months where there is more traffic in general. (if a product is bought and looked at 20 % more than
#  average in a given month, but on average all products were bought and looked at 20 % more in that month, the traffic
#  for the product should not be considered above average) -> also find a better way to formulate this.


# update table
def create_column_popular_months(sql_connection, sql_cursor):
    sql_query = """ALTER TABLE products
ADD popular_month VARCHAR;"""
    sql_cursor.execute(sql_query)
    sql_connection.commit()


def update_popular_month_query():
    return """UPDATE products AS p
    SET popular_month = %s
    WHERE product__id = %s"""


#
def get_popular_months(traffic_per_month):
    """"""
    bar = traffic.get_bar_product(traffic_per_month)
    popular_months = ''

    for traffic_month in traffic_per_month:
        if traffic_month >= bar:
            # gets the month by finding the index of the traffic and adding one, as the traffic of month 1 is indexed on
            # index 0 and so on.
            popular_month = str(traffic_per_month.index(traffic_month) + 1)
            popular_months += ', {}'.format(popular_month)

    if popular_months:
        return popular_months[2:]


def calculate_popular_months_products(sql_cursor):
    """"""
    products_query = sql_l.all_product_ids_query()
    sql_cursor.execute(products_query)
    months = [str(i) for i in range(1, 13)]
    product_popular_month = tuple()
    for product in [product_id[0] for product_id in sql_cursor.fetchall()]:
        traffic_per_month = traffic.get_traffic_all_months_all_time(product, months)
        popular_months = get_popular_months(traffic_per_month)
        product_popular_month += ((popular_months, product),)

    return product_popular_month


def initiate_popular_months():
    """"""
    sql_connection, sql_cursor = sql_c.connect()

    create_column_popular_months(sql_connection, sql_cursor)

    product_popular_months = calculate_popular_months_products(sql_cursor)

    update_pop_month = update_popular_month_query()
    sql_cursor.execute(update_pop_month, product_popular_months)

    sql_connection.commit()


def update_popular_months():
    """"""
    sql_connection, sql_cursor = sql_c.connect()

    product_popular_months = calculate_popular_months_products(sql_cursor)

    update_pop_month = update_popular_month_query()
    sql_cursor.executemany(update_pop_month, product_popular_months)

    sql_connection.commit()


if __name__ == '__main__':
    update_popular_months()
