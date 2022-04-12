import PostgreSQL.load.products.load_products as load_products
import random
import PostgreSQL.connect_postgresql_database as sql_c
import json

random_sample_file = 'C:\\Users\\sfjbr\\PycharmProjects\\project_blok_c\\Validation\\samples.json'


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


def load_samples(sample_type='random_samples'):
    with open(random_sample_file, 'r') as json_open:
        samples = json.load(json_open)
    return samples[sample_type]


def make_random_samples_file():
    with open(random_sample_file, 'w+') as json_open:
        con, cur = sql_c.connect()
        samples = {'random_samples': load_random_products(cur)}
        json.dump(samples, json_open, indent=4)
        sql_c.disconnect(con, cur)


if __name__ == '__main__':
    print(load_samples())
