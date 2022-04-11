def product_gender():
    sql = f'SELECT product__id FROM products WHERE gender = (SELECT gender FROM products WHERE product__id = %s) AND ' \
          f'product__id != %s;'
    return sql


def product_price():
    sql = f'SELECT selling_price FROM products WHERE selling_price = (SELECT selling_price FROM products WHERE ' \
          f'product__id = %s) AND product__id != %s;'
    return sql
