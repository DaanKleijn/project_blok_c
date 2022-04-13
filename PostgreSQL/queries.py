def product_gender():
    sql = f'SELECT product__id FROM products WHERE gender = (SELECT gender FROM products WHERE product__id = %s) ' \
          f'AND product__id != %s ' \
          f'AND category = (SELECT category FROM products WHERE product__id = %s)'

    return sql


def product_price():
    sql = f'SELECT selling_price FROM products WHERE product__id = CAST (%s AS VARCHAR);'
    return sql


def new_product_price_query():
    sql = f'SELECT product__id FROM products WHERE selling_price >= %s AND selling_price <= %s  AND product__id != %s;'
    return sql