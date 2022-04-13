# This file is dedicated to fetching data about products out of the SQL database.

import PostgreSQL.load.products.queries as product_queries
import PostgreSQL.connect_postgresql_database as sql_c


def all_product_ids(sql_cursor):
    """Takes an SQL cursor as input. Fetches all product ids of products in categories and returns them."""
    product_query = product_queries.product_ids_in_categories()
    sql_cursor.execute(product_query)
    return [product[0] for product in sql_cursor.fetchall()]


def ordered_together_with(product, sql_cursor):
    """
    Takes a product_id (str) and SQL cursor as input. Fetches the product_id of all products ordered together with the
    input product, specified with id. Returns all fetched products (list) [str].
    """
    products_query = product_queries.event_product_query()
    sql_cursor.execute(products_query, (product, 'ordered', 'ordered', product))
    return [ordered_product[0] for ordered_product in sql_cursor.fetchall()]


def date_filtered(month, sql_cursor):
    """
    Takes a month, written as integer (str) and an SQL cursor as input. Fetches all products, popular in the given
    month from the database and returns them.
    """
    product_query = product_queries.product_pop_month_query().format(month)
    sql_cursor.execute(product_query)

    return [product[0] for product in sql_cursor.fetchall()]


def get_properties(product_ids, sql_cursor):
    """
    Takes a list with product ids (list) [str] and an SQL cursor as input. Loads the properties of all products in from
    the database.
    Composes a list with tuples, containing the product_properties, the sub_category and the product id for each
    product. When there is no sub_category, replaces the sub_category with the category.
    Returns this list (list) [((str, str, str ...), str, str)].
    """
    prop_query = product_queries.properties_multiple_query().format(','.join(['%s'] * len(product_ids)))
    sql_cursor.execute(prop_query, product_ids)
    return [(properties[3:], properties[2], properties[0])
            if not properties[1]
            else (properties[3:], properties[1], properties[0])
            for properties in sql_cursor.fetchall()]


if __name__ == '__main__':
    con, cur = sql_c.connect()
    print(date_filtered('2', cur))
    sql_c.disconnect(con, cur)
