import Validation.date_helper as date_helper
import Validation.data_conversion as convert_data
import PostgreSQL.connect_postgresql_database as sql_c
import recommend
from datetime import datetime

json_validation_file = 'trending validation set.json'


def random_sampling(sql_cursor, amount=10):
    """"""
    random_dates = date_helper.get_random_dates('2017-12-1', '2018-12-31', amount)
    big_dict = {}
    for random_date in random_dates:
        big_dict[random_date.strftime('%Y-%m-%d')] = recommend.products_trending_date(amount=20,
                                                                                      date=random_date,
                                                                                      sql_cursor=sql_cursor)

    convert_data.samples_other_dict(products=big_dict,
                                    sql_cursor=sql_cursor,
                                    json_file=json_validation_file)


if __name__ == '__main__':
    con, cur = sql_c.connect()
    random_sampling(cur)

