import PostgreSQL.connect_postgresql_database as sql_c
import PostgreSQL.queries as sql_query
import time
import psycopg2.extras
import similar_properties as similar


def properties_multiple_query():
    """"""
    return """SELECT product__id, sub_category, category, brand, color, flavor, doelgroep, eenheid, factor, 
    geschiktvoor, geursoort, huidconditie, huidtype, huidtypegezicht, klacht, kleur, leeftijd, soort, 
    soorthaarverzorging, soortmondverzorging, sterkte, product_type, typehaarkleuring, typetandenbostel, variant, 
    waterproof FROM products 
    WHERE product__id IN ({});"""


def insert_similar_query():
    return """INSERT INTO similars
    VALUES (%s, %s)"""


def get_properties(product_ids, sql_cursor):
    """"""""
    prop_query = properties_multiple_query().format(','.join(['%s'] * len(product_ids)))
    sql_cursor.execute(prop_query, product_ids)
    return [(properties[3:], properties[2], properties[0])
            if not properties[1]
            else (properties[3:], properties[1], properties[0])
            for properties in sql_cursor.fetchall()]


def split_sub_categories(big_list):
    """"""
    big_matrix = dict()
    for i in range(len(big_list)):
        try:
            big_matrix[big_list[i][1]][big_list[i][2]] = big_list[i][0]
        except KeyError:
            big_matrix[big_list[i][1]] = dict()
            big_matrix[big_list[i][1]][big_list[i][2]] = big_list[i][0]
    del big_matrix[None]

    return big_matrix


def compile_all_similars(sql_cursor, sql_connection, amount=4):
    """"""
    sql_cursor.execute(sql_query.all_product_ids_query())
    products = sql_cursor.fetchall()
    properties = get_properties(products, sql_cursor)
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
    similar_update_query = insert_similar_query()
    psycopg2.extras.execute_batch(sql_cursor, similar_update_query, similar_values, page_size=10000)
    sql_connection.commit()
    print('similar products are committed to the sql database')


if __name__ == '__main__':
    start_time = time.time_ns()
    con, cur = sql_c.connect()
    compile_all_similars(cur, con)
    sql_c.disconnect(con, cur)
    print('The program took {:.4f} seconds to complete'.format((time.time_ns() - start_time) / 1000000000))
