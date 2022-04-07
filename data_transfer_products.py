import MongoDB.connect_mongodb as mdb_c
import PostgreSQL.connect_postgresql_database as sql_c
import transfer_functions as shared
import psycopg2.extras


# query
def create_product_query():
    """Creates an sql query to insert the desired data in the products table and returns this query."""
    return """
    INSERT INTO  products (product__id, product_name, brand, category, color, flavor, gender, herhaalaankopen, 
    recommendable, sub_category, sub_sub_category, sub_sub_sub_category, selling_price, availability, 
    doelgroep, factor, geschiktvoor, geursoort, huidconditie, huidtype, huidtypegezicht, klacht, 
    kleur, leeftijd, soort, soorthaarverzorging, soortmondverzorging, sterkte, product_type, typehaarkleuring, 
    typetandenbostel, variant, waterproof) 
    VALUES ({} %s);
    """.format('%s,' * 32)


# fetch values
def get_product_values(product):
    """Takes a product (dict) as input. Selects all wanted data and returns this (tuple)."""
    result = tuple()
    wanted_fields = ['_id', 'name', 'brand', 'category', 'color', 'flavor', 'gender', 'herhaalaankopen',
                     'recommendable', 'sub_category', 'sub_sub_category', 'sub_sub_sub_category']

    wanted_price_fields = ['selling_price']

    wanted_property_fields = ['availability', 'doelgroep', 'factor', 'geschiktvoor', 'geursoort',
                              'huidconditie', 'huidtype', 'huidtypegezicht', 'klacht', 'kleur', 'leeftijd', 'soort',
                              'soorthaarverzorging', 'soortmondverzorging', 'sterkte', 'type', 'typehaarkleuring',
                              'typetandenbostel', 'variant', 'waterproof']

    for field in wanted_fields:
        result += (shared.secure_dict_fetch(product, field),)
    for field in wanted_price_fields:
        result += (shared.secure_dict_fetch_double(product, 'price', field),)
    for field in wanted_property_fields:
        result += (shared.secure_dict_fetch_double(product, 'properties', field),)

    return result


# upload
def upload_product(product):
    """Takes information about a product (dict) as input. Uploads the product to the local sql database."""
    connection, cursor = sql_c.connect()
    sql_query = create_product_query()
    values_to_insert = get_product_values(product)
    cursor.execute(sql_query, values_to_insert)
    connection.commit()
    sql_c.disconnect(connection, cursor)


def upload_all_products():
    """Loads all products from the local mongodb database. Uploads the products to the local sql database."""
    print('start')
    database = mdb_c.connect()
    products_collection = database.products
    sql_connection, sql_cursor = sql_c.connect()
    sql_query = create_product_query()
    values_to_insert = []
    for product in products_collection.find():
        values_to_insert.append(get_product_values(product))
    print('Data is compiled')
    psycopg2.extras.execute_batch(sql_cursor, sql_query, values_to_insert, page_size=10000)
    print('products table is updated')
    sql_connection.commit()
    print('Data is committed')
    sql_c.disconnect(sql_connection, sql_cursor)


if __name__ == '__main__':
    upload_all_products()
