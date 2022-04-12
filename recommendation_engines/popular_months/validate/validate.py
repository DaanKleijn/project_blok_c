import PostgreSQL.connect_postgresql_database as sql_c
import Validation.data_conversion as convert_data
import recommendation_engines.popular_months.recommend as popular_months

random_validation_file = 'complete_validation_set.json'
mandatory_validation_file = 'mandatory_validation_set.json'


def get_samples(sql_cursor):
    months = [str(month) for month in range(1, 13)]
    result = {}
    print(months)
    for month in months:
        result[month] = popular_months.recommended_products_month(month=month,
                                                                  product_amount=500,
                                                                  sql_cursor=sql_cursor)
    return result


def take_samples():
    sql_connection, sql_cursor = sql_c.connect()
    validation_products = get_samples(sql_cursor)
    convert_data.samples_other_dict(products=validation_products,
                                    sql_cursor=sql_cursor,
                                    json_file=random_validation_file)
    sql_c.disconnect(sql_connection, sql_cursor)


if __name__ == '__main__':
    take_samples()
