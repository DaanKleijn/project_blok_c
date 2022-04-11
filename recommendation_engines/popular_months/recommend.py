from datetime import datetime
import PostgreSQL.load.products.load_products as load_products
import PostgreSQL.connect_postgresql_database as sql_c


def recommend(product_amount, sql_cursor):
    """
    Takes the amount of desired products (int) as input.
    Fetches products that are more popular during the current month than in other months.
    A more popular month gets 40 % + 50 more sales than an average month.
    Returns the desired amount of products (list) [str].
    """
    month = str(int(datetime.today().strftime('%m')))
    trending_products = load_products.date_filtered(month, sql_cursor)
    if len(trending_products) >= product_amount:
        return trending_products[:product_amount]
    return trending_products


if __name__ == '__main__':
    con, cur = sql_c.connect()
    print(recommend(100, cur))
    sql_c.disconnect(con, cur)
