import PostgreSQL.connect_postgresql_database as connect


def create_table(name, column_names):
    sql = f'CREATE TABLE {name} (' + ','.join(column_names) + ')'
    return sql


def create_column_names(name, type, flags):
    return f'{name}, {type}, {flags}'


def create_columns(columns):
    column_lst = []
    for i in columns:
        column_lst.append(create_column_names(i[0], i[1], i[2]))
    return column_lst


connection = connect.connect_postgresql_database(host='localhost', database='huwebshop', user='postgres', password='postgres')

columns = [
    ['id', 'VARCHAR(32)', 'NOT NULL'],
    ['name', 'VARCHAR(255)', ''],
    ['price', 'INT', ''],
    ['category', 'VARCHAR(255)', ''],
    ['gender', 'VARCHAR(10)', '']
]
column_list = create_columns(columns)

sql = create_table(name='products', column_names=column_list)

cursor = connection.cursor()
cursor.execute(sql)
cursor.close()
connection.commit()