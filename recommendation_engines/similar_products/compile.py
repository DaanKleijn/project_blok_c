# This file is dedicated to compiling similar products for every product in the database and writing these values to the
# database's similars table.

import PostgreSQL.connect_postgresql_database as sql_c
import PostgreSQL.load.products.load_products as load_products
import PostgreSQL.insert.similars as insert_similar
import time
import similar_properties as similar

# Before running this file, you have to create the similars table in SQL by creating it manually. You can also run
# create_similar_product_table.ddl, which can be found in subdirectory create in directory PostgreSQL


def split_sub_categories(product_list):
    """
    Takes a list containing tuples as input. The tuple contains product_data on the first index, the category the
    product belongs to on the second and a product_id on the third index.
    Creates a dictionary with the following structure: {category: {product_id: product_data}} and returns this (dict)
    {str: {str: tuple}}.
    """
    product_data = dict()
    # cycles for all products
    for i in range(len(product_list)):
        # tries to record the product in the dict under their category key
        try:
            product_data[product_list[i][1]][product_list[i][2]] = product_list[i][0]
        # creates category key when it doesn't exist and records product under it.
        except KeyError:
            product_data[product_list[i][1]] = dict()
            product_data[product_list[i][1]][product_list[i][2]] = product_list[i][0]

    return product_data


def compile_all_similars(sql_cursor, sql_connection, product_amount=4):
    """
    Takes an sql_cursor and connection as input. You can optionally set the amount of similar products you want to
    compile (set to 4 when no amount is specified).
    Fetches all product_ids recorded in the database. Also fetches the properties of all products.
    Compiles a product_amount number of similar products with these values. Writes these similar products in the
    similars table, together with the original product. Does not return anything.
    """
    # loads all product_ids
    products = load_products.all_product_ids(sql_cursor)
    # loads all product properties
    properties = load_products.get_properties(products, sql_cursor)
    print('fetched unprocessed properties')
    # loads products with their properties in a dict where i can better access them.
    properties_dict = split_sub_categories(properties)
    print('processed properties into a dict')
    similar_values = []
    # cycles through every category, taking the category name and all products contained in the category.
    for category, category_products in iter(properties_dict.items()):
        # cycles through every product (contained in the category), taking the product_id and product_properties
        for product_id, properties in iter(category_products.items()):
            # fetches products similar to the product
            similars = similar.get_similars(product_id, properties, category_products, product_amount)

            # saves all similar products to a list with the product_id of the product it is recommended with.
            for similar_value in similars:
                similar_values.append((product_id, similar_value))
        print('{} done'.format(category))
    print('calculated all similar products')
    # uploads similar products to the database.
    insert_similar.upload_similar(sql_cursor, similar_values)
    sql_connection.commit()
    print('similar products are committed to the sql database')


if __name__ == '__main__':
    # Before running this file, you have to create the similars table in SQL by creating it manually. You can also run
    # create_similar_product_table.ddl, which can be found in subdirectory create in directory PostgreSQL
    start_time = time.time_ns()
    con, cur = sql_c.connect()
    compile_all_similars(cur, con)
    sql_c.disconnect(con, cur)
    print('The program took {:.4f} seconds to complete'.format((time.time_ns() - start_time) / 1000000000))
