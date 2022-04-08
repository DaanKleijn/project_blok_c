import PostgreSQL.connect_postgresql_database as sql_c
import json

pop_months_json_file = 'bought_and_viewed_popular_months.json'

con, cur = sql_c.connect()
cur.execute("""SELECT product__id, popular_month FROM products""")

list_pop_months = cur.fetchall()

insert_dict = {'popular months': list_pop_months}

with open(pop_months_json_file, 'w+') as open_json:
    json.dump(insert_dict, open_json, indent=4)
