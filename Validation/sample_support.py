import PostgreSQL.load.products.load_products as load_products
import random


def load_random_products(sql_cursor, amount=20):
    """"""
    all_products = load_products.all_product_ids(sql_cursor)
    random_products = []
    amount_of_products = len(all_products)
    items_fetched = 0
    while items_fetched < amount:
        rand_int = random.randint(0, amount_of_products)
        random_products.append(all_products[rand_int])
        del all_products[rand_int]
        amount_of_products -= 1
        items_fetched += 1

    return random_products