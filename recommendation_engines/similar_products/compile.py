import PostgreSQL.connect_postgresql_database as sql_c
import PostgreSQL.load.products.load_products as load_products
import PostgreSQL.insert.similars as insert_similar
import time
import similar_properties as similar


def split_sub_categories(big_list):
    """"""
    big_matrix = dict()
    for i in range(len(big_list)):
        try:
            big_matrix[big_list[i][1]][big_list[i][2]] = big_list[i][0]
        except KeyError:
            big_matrix[big_list[i][1]] = dict()
            big_matrix[big_list[i][1]][big_list[i][2]] = big_list[i][0]

    return big_matrix


def compile_all_similars(sql_cursor, sql_connection, amount=4):
    """"""
    products = load_products.all_product_ids(sql_cursor)
    properties = load_products.get_properties(products, sql_cursor)
    print('fetched unprocessed properties')
    properties_dict = split_sub_categories(properties)
    print('processed properties into a dict')
    similar_values = []
    print('Categories are {}'.format(list(properties_dict.keys())))
    for category, category_products in iter(properties_dict.items()):
        for product_id, properties in iter(category_products.items()):
            similars = similar.get_similars(product_id, properties, category_products, amount)
            for similar_value in similars:
                similar_values.append((product_id, similar_value))
        print('{} done'.format(category))
    print('calculated all similar products')
    insert_similar.upload_similar(sql_cursor, similar_values)
    sql_connection.commit()
    print('similar products are committed to the sql database')


if __name__ == '__main__':
    start_time = time.time_ns()
    con, cur = sql_c.connect()
    compile_all_similars(cur, con)
    sql_c.disconnect(con, cur)
    print('The program took {:.4f} seconds to complete'.format((time.time_ns() - start_time) / 1000000000))
