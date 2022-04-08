from load_data_sql import product_price, product_gender
import random
import PostgreSQL.connect_postgresql_database as sql_c

selling_price = product_price()


def simular_gender(product_id):
    con, cur = sql_c.connect()
    product_query = product_gender()
    cur.execute(product_query, (product_id, product_id))
    similar_products = [product_id[0] for product_id in cur.fetchall()]

    index = random.randint(0, len(similar_products))
    new_product_gender = similar_products[index]

    return new_product_gender


def simular_price(product_id):
    con, cur = sql_c.connect()
    product_query = product_gender()
    cur.execute(product_query, (product_id, product_id))
    similar_products = [product_id[0] for product_id in cur.fetchall()]
    index = random.randint(0, len(similar_products))
    new_product_price = similar_products[index]

    return new_product_price


if __name__ == '__main__':
    print(simular_gender('16121'))
    print(simular_price('16121'))