from PostgreSQL.queries import product_gender,  product_price, new_product_price_query
import random
import PostgreSQL.connect_postgresql_database as sql_c


def simular_gender(product_id, amount=4):
    con, cur = sql_c.connect()
    product_query = product_gender()
    cur.execute(product_query, (product_id, product_id, product_id, ))
    similar_products = [product_id[0] for product_id in cur.fetchall()]
    new_product_gender_list = []

    for i in range(0, amount):
        index = random.randint(0, len(similar_products))
        try:
            new_product_gender = similar_products[index]
            new_product_gender_list.append(new_product_gender)
        except IndexError:
            break

    return new_product_gender_list


def simular_price(product_id, amount=4):

    con, cur = sql_c.connect()
    product_query = product_price()
    cur.execute(product_query, (product_id,))
    price = cur.fetchall()[0][0]
    min_price = price * 0.75
    max_price = price * 1.25
    new_product_list = []

    new_product_query = new_product_price_query()
    cur.execute(new_product_query, (min_price, max_price, product_id,))
    simular_products = [product_id[0] for product_id in cur.fetchall()]

    for i in range(0, amount):
        index = random.randint(0, len(simular_products))
        try:
            new_product_price = simular_products[index]
            new_product_list.append(new_product_price)
        except IndexError:
            break

    return new_product_list


if __name__ == '__main__':
    print(simular_gender('7189'))
    print(simular_price('7189'))
