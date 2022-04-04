import PostgreSQL.connect_postgresql_database as connect

connection = connect.connect_db(host = 'localhost', database = 'postgres', user = 'postgres', password = 'password')



def get_products(connection, product_ids):
    products = []
    cursor = connection.cursor()
    for id in product_ids:
        cursor.exucute(f"SELECT * FROM products where id = '{id}'")
        products.append(cursor.fetchall())
    cursor.close
    return products
