import load_data_sql as product_info
import load_data_sql as selling_price
import random

def simular_gender(product_info):
    product_lst = []
    for i in range(product_info):
        product_lst.append(product_info)
    index = random.randint(0, len(product_lst))
    new_product = product_lst[index]
    if new_product == product_info:
        index = random.randint(0, len(product_lst))
        new_product = product_lst[index]
        return new_product
    return new_product


def simular_price(selling_price):
    product_lst = []
    for i in range(selling_price):
        product_lst.append(selling_price)
    index = random.randint(0, len(product_lst))
    new_product = product_lst[index]
    if new_product == selling_price:
        index = random.randint(0, len(product_lst))
        new_product = product_lst[index]
        return new_product
    return new_product