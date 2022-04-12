def wanted_valuation_values_query():
    """"""
    return """SELECT product__id, product_name, category, sub_category, sub_sub_category, sub_sub_sub_category 
    FROM products 
    WHERE product_id IN ({});"""


def get_validation_dict(products, sql_cursor):
    """"""
    query = wanted_valuation_values_query()
    sql_cursor.execute(query, products)
    return [{'product_id': product_info[0],
      'name': product_info[1],
      'category': product_info[2],
      'sub_category': product_info[3],
      'sub_sub_category': product_info[4],
      'sub_sub_sub_category': product_info[5] } for product_info in sql_cursor.fetchall()]
