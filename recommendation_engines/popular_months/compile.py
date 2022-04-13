import time
import PostgreSQL.connect_postgresql_database as sql_c
import PostgreSQL.load.products.queries as load_products
import PostgreSQL.load.traffic.load_traffic as traffic
import PostgreSQL.insert.popular_month as update_sql

# TODO: account for months where there is more traffic in general. (if a product is bought and looked at 20 % more than
#  average in a given month, but on average all products were bought and looked at 20 % more in that month, the traffic
#  for the product should not be considered above average) -> also find a better way to formulate this.


def get_overall_bar(traffic_per_month):
    """
    Takes a list with 12 count values (list) [int] as input. Each value represents the amount of hits a given product
    has ever received during a month.
    Calculates the minimum amount of times a product has be sold any given month for that traffic to be significant.
    (140 % + 50)
    """
    average_traffic = sum(traffic_per_month) / 12
    return average_traffic * 1.4 + 50


def get_popular_months(traffic_per_month):
    """
    Takes a list with traffic per month (list) [int] for a product as input.
    Calculates if any month gets significantly more traffic than other months.
    Returns these months as integers in a formatted string. (e.g. '4, 5');
    returns None if no popular months are found.
    """
    # gets amount of traffic the month has to beat to be significant
    bar = get_overall_bar(traffic_per_month)
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
    Takes an SQL cursor as input.
    Fetches all product_ids. Fetches the amount of times the product has been sold per month, per product. Calculates
    per product if there are months with significantly higher traffic (products sold per month).
    Significant is 140% + 50 amount of sales.
    Adds the popular_months and product_id in a tuple to a list.
    Returns this list [(str, str)].
    """
    products_query = load_products.all_product_ids_query()
    sql_cursor.execute(products_query)
    months = [str(i) for i in range(1, 13)]
    product_popular_months = list()

    products = [str(product[0]) for product in sql_cursor.fetchall()]
    all_traffic = traffic.get_all_traffic_per_month(products, months, sql_cursor)
    # cycles through all products
    for product in products:
        product_traffic = list()
        # cycles for every month
        for month_index in range(12):
            # tries to fetch the number of sales from the traffic dictionary. Adds it to the traffic list.
            try:
                product_traffic.append(all_traffic[str(month_index)][product])
            # if this product has never been sold in this month, adds a zero to the traffic list
            except KeyError:
                product_traffic.append(0)
        # calculates if some months are more popular than others, using the traffic list.
        pop_months = get_popular_months(product_traffic)
        # adds these popular months with the product_id in a tuple to the list we want to return.
        product_popular_months.append((pop_months, product))

    return product_popular_months


def initiate_popular_months(sql_connection, sql_cursor):
    """
    Takes an SQL connection and cursor as input.
    In the SQL database, creates the popular_month column in the products table.
    Fetches products. Per product, fetches the amount of times it has been sold in the past (ever). Calculates per
    product if they are sold significantly more in certain months. Updates the popular_month column in
    the product table with this value.
    """
    update_sql.create_column_popular_months(sql_connection, sql_cursor)

    return update_popular_months(sql_connection, sql_cursor)


def update_popular_months(sql_connection, sql_cursor):
    """
    Takes an SQL connection and cursor as input.
    Fetches products. Per product, fetches the amount of times it has been sold in the past (ever). Calculates per
    product if they are sold significantly more in certain months.
    Updates the popular_month column in the product table with this value.
    """
    start_time = time.time_ns()

    product_popular_months = calculate_popular_months_products(sql_cursor)
    update_sql.update_popular_month(sql_cursor, product_popular_months)

    sql_connection.commit()
    return '{:.4f} secondes'.format((time.time_ns() - start_time) / 1000000000)


if __name__ == '__main__':
    con, cur = sql_c.connect()
    print(update_popular_months(con, cur))
    sql_c.disconnect(con, cur)
