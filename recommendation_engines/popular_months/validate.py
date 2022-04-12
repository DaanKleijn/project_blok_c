import PostgreSQL.connect_postgresql_database as sql_c
import Validation.sample_support as sample_support
import Validation.data_conversion as convert_data
import recommend as popular_months

json_validation_file = 'validation_set.json'


def get_samples(sql_cursor):
    months = [str(month) for month in range(1, 13)]
    result = {}
    for month in months:
        result[month] = popular_months.recommended_products(product_amount=50,
                                                            sql_cursor=sql_cursor)
    return result


if __name__ == '__main__':
    con, cur = sql_c.connect()
    validation_products = get_samples(cur)
    convert_data.samples_other_dict(products=validation_products,
                                      sql_cursor=cur,
                                      json_file=json_validation_file)
    sql_c.disconnect(con, cur)
