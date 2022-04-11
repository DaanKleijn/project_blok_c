import PostgreSQL.load.products.queries as product_queries
import PostgreSQL.load.sessions.queries as session_queries


def all_product_ids(sql_cursor):
    """Takes an sql cursor as input. Fetches all product ids and returns them."""
    product_query = product_queries.product_ids_in_categories()
    sql_cursor.execute(product_query)
    return [product[0] for product in sql_cursor.fetchall()]


def ordered_together_with(product, sql_cursor):
    """
    Takes a product_id as input. Fetches the product_id of all products ordered together with the input product.
    Returns all fetched products (list) [str].
    """
    products_query = session_queries.event_product_query()
    sql_cursor.execute(products_query, (product, 'ordered', product))
    return [ordered_product[0] for ordered_product in sql_cursor.fetchall()]


def date_filtered(month, sql_cursor):
    """"""
    product_query = product_queries.product_pop_month_query()
    sql_cursor.execute(product_query.format(month))

    return [product[0] for product in sql_cursor.fetchall()]


def get_properties(product_ids, sql_cursor):
    """"""""
    prop_query = product_queries.properties_multiple_query().format(','.join(['%s'] * len(product_ids)))
    sql_cursor.execute(prop_query, product_ids)
    return [(properties[3:], properties[2], properties[0])
            if not properties[1]
            else (properties[3:], properties[1], properties[0])
            for properties in sql_cursor.fetchall()]
