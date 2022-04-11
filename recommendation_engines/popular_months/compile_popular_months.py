import time
import PostgreSQL.connect_postgresql_database as sql_c
import PostgreSQL.queries as sql_query
import recommendation_engines.product_traffic as traffic

# TODO: account for months where there is more traffic in general. (if a product is bought and looked at 20 % more than
#  average in a given month, but on average all products were bought and looked at 20 % more in that month, the traffic
#  for the product should not be considered above average) -> also find a better way to formulate this.


# update table
def create_column_popular_months(sql_connection, sql_cursor):
    """Returns a query that adds the column 'popular_month' to the products table."""
    sql_query = """ALTER TABLE products
    ADD popular_month VARCHAR;"""
    sql_cursor.execute(sql_query)
    sql_connection.commit()


def update_popular_month_query():
    """
    Returns a query that updates 'popular_month' of a given product_id to a given value.
    Format order is month_value, product_id.
    """
    return """UPDATE products
    SET popular_month = %s
    WHERE product__id = %s"""


def get_popular_months(traffic_per_month):
    """
    Takes a list with traffic per month (list) [int] for a product as input. Calculates if any month gets significantly
    more traffic than other months.
    Returns these months as integers in a formatted string. (e.g. '4, 5'); returns None if no popular months are found.
    """
    bar = traffic.get__overall_bar(traffic_per_month)
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
    """
    Fetches all product_ids. Fetches the amount of times the product has been sold per month, per product. Calculates
    per product if there are months with significantly more traffic (products sold per month). Significant is 140% + 50
    amount of sales. Adds the popular_months and product_id in a tuple to a list.
    Returns this list [(str, str)].
    """
    products_query = sql_query.all_product_ids_query()
    sql_cursor.execute(products_query)
    months = [str(i) for i in range(1, 13)]
    product_popular_months = list()

    products = [str(product[0]) for product in sql_cursor.fetchall()]
    all_traffic = traffic.get_all_traffic(products, months)
    for product in products:
        product_traffic = list()
        for month_index in range(12):
            try:
                product_traffic.append(all_traffic[str(month_index)][product])
            except KeyError:
                product_traffic.append(0)
        pop_months = get_popular_months(product_traffic)
        product_popular_months.append((pop_months, product))

    return product_popular_months


def initiate_popular_months():
    """
    In the SQL database, creates the popular_month column in the products table.
    Fetches products and their past traffic. Traffic is made out of unique purchases.
    Calculates per product if they are sold significantly more in certain months. Updates the popular_month column in
    the product table with this value.
    """
    sql_connection, sql_cursor = sql_c.connect()

    create_column_popular_months(sql_connection, sql_cursor)

    product_popular_months = calculate_popular_months_products(sql_cursor)
    update_pop_month = update_popular_month_query()
    sql_cursor.execute(update_pop_month, product_popular_months)

    sql_connection.commit()


def update_popular_months():
    """
    Fetches products and their past traffic. Traffic is made out of unique purchases.
    Calculates per product if they are sold significantly more in certain months. Updates the popular_month column in
    the product table with this value.
    """
    start_time = time.time_ns()
    sql_connection, sql_cursor = sql_c.connect()

    product_popular_months = calculate_popular_months_products(sql_cursor)

    update_pop_month = update_popular_month_query()
    sql_cursor.executemany(update_pop_month, product_popular_months)

    sql_connection.commit()
    return '{:.4f} secondes'.format((time.time_ns() - start_time) / 1000000000)


if __name__ == '__main__':
    print(update_popular_months())
