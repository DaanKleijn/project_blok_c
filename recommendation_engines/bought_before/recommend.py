import psycopg2
import json
import random


def connect_sql():
    connection = psycopg2.connect(host='localhost',
                                  database='RE_webshop',
                                  user='postgres',
                                  password='kasper18')

    cursor = connection.cursor()
    return connection, cursor


def disconnect_sql(cursor, connection):
    cursor.close()
    connection.close()


def profiles_select(profile_id):
    '''
    Op basis van de profile_id ga ik kijken naar de sessies die deze gebruiker heeft gedaan
    argument: = profile_id
    return: = buid (tuple)
    '''
    sql_connection, sql_cursor = connect_sql()
    profile_query = f"SELECT profile_buids FROM profiles WHERE profile__id = '{profile_id}'"
    sql_cursor.execute(profile_query)
    buids = sql_cursor.fetchall()
    disconnect_sql(sql_connection, sql_cursor)
    return buids


def sessions_select(profile_id):
    '''
    Op basis van de profile_buids kijk ik in de session tabel om te kijken welke producten zijn gekocht (dus alleen als has_sale true is)
    argument: profile_id
    return: lijst met producten
    '''
    buids = list(profiles_select(profile_id)[0])[0].split(',')
    sql_connection, sql_cursor = connect_sql()
    all_products = []
    for buid in buids:
        if '{' in buid:
            buid = buid[1:]
        if '}' in buid:
            buid = buid[0:-1]
        buids_query = f"SELECT session_products FROM sessions WHERE session_buid = '{buid}' and sale = true"
        sql_cursor.execute(buids_query)
        products = json.loads(sql_cursor.fetchall()[0][0])
        all_products.extend(products)
    disconnect_sql(sql_connection, sql_cursor)
    return all_products


def products_select(profile_id):
    '''
    Op basis van de product ids die een profiel heeft gekocht wordt hier de info over producten opgehaald
    argument: profile_id:
    return: list with product info
    '''
    product_list = sessions_select(profile_id)
    sql_connection, sql_cursor = connect_sql()
    product_info = []
    for product in product_list:
        product_query = f"SELECT product_brand, product_category, product_sub_category, product_sub_sub_category" \
                        f" FROM products WHERE product__id = '{product}'"
        sql_cursor.execute(product_query)
        product = sql_cursor.fetchall()[0]
        product_info.append(product)
    disconnect_sql(sql_connection, sql_cursor)
    return product_info


def product_info(profile_id):
    '''
    Op basis van de producten die een gebruiken heeft gekocht worden hier de details die een bepaalde gebruiker het meest
    koopt achterhaald
    argument: profile_id
    return: meest gekochte brand, category, sub_category, sub_sub_category
    '''
    product_list = products_select(profile_id)
    all_brands, all_category, all_sub_category, all_sub_sub_category = [], [], [], []
    count = 0
    for product_brand in product_list:
        brand = product_brand[0]
        all_brands.append(brand)
    for brand in all_brands:
        frequency = all_brands.count(brand)
        if frequency > count:
            count = frequency
            best_brand = brand
    count = 0
    for product_cat in product_list:
        category = product_cat[1]
        all_category.append(category)
    for category in all_category:
        frequency = all_category.count(category)
        if frequency > count:
            count = frequency
            best_category = category
    count = 0
    for product_sub_cat in product_list:
        sub_category = product_sub_cat[2]
        all_sub_category.append(sub_category)
    for sub_category in all_sub_category:
        frequency = all_sub_category.count(sub_category)
        if frequency > count:
            count = frequency
            best_sub_category = sub_category
    count = 0
    for product_sub_sub_category in product_list:
        sub_sub_category = product_sub_sub_category[3]
        all_sub_sub_category.append(sub_sub_category)
    for sub_sub_category in all_sub_sub_category:
        frequency = all_sub_sub_category.count(sub_sub_category)
        if frequency > count:
            count = frequency
            best_sub_sub_category = sub_sub_category
    return best_brand, best_category, best_sub_category, best_sub_sub_category


def product_recommendation(profile_id):
    '''
    Op basis van de meest voorkomende details van een product gaan we kijken of andere producten vergelijkbaar zijn
    argument: profile_id
    return: product_ids
    '''
    brand, category, sub_category, sub_sub_category = product_info(profile_id)
    sql_connection, sql_cursor = connect_sql()
    product_search_query = f"SELECT product__id FROM products WHERE product_brand = '{brand}' AND product_category = '{category}'"
    sql_cursor.execute(product_search_query)
    product_ids = sql_cursor.fetchall()
    if len(product_ids) > 4:
        product_search_query_2 = f"SELECT product__id FROM products WHERE product_brand = '{brand}' AND product_sub_category = '{sub_category}' "
        sql_cursor.execute(product_search_query_2)
        product_ids_2 = sql_cursor.fetchall()
        if len(product_ids_2) > 4:
            product_search_query_3 =  f"SELECT product__id FROM products WHERE product_brand = '{brand}'" \
                                      f" AND product_sub_category = '{sub_category}' AND NOT product_sub_sub_category = '{sub_sub_category}'"
            sql_cursor.execute(product_search_query_3)
            product_ids_3 = sql_cursor.fetchall()
            disconnect_sql(sql_connection, sql_cursor)
            return product_ids_3
        else:
            disconnect_sql(sql_connection, sql_cursor)
            return product_ids_2
    else:
        disconnect_sql(sql_connection, sql_cursor)
        return product_ids


def final_recommendation(profile_id):
    '''
    Hier worden 4 random producten gekozen die vergelijkbaar zijn met de gekochte producten
    argument: profile_id
    return: recommendation_list (4 products)
    '''
    recommendations = product_recommendation(profile_id)
    product_list = sessions_select(profile_id)
    recommendations_string = []
    for recommendation in recommendations:
        recommendation = recommendation[0]
        recommendations_string.append(recommendation)
    for product in product_list:
        if product in recommendations_string:
            recommendations_string.remove(product)
    recommendation_list = []
    random_list = [random.randrange(0, len(recommendations_string), 1), random.randrange(0, len(recommendations_string), 1), random.randrange(0, len(recommendations_string), 1), random.randrange(0, len(recommendations_string), 1)]
    for index in random_list:
        product = recommendations_string[index]
        recommendation_list.append(product)
    return recommendation_list
