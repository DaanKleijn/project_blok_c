# This file is dedicated to fetching random dates between specified dates.

import random
import time
from datetime import datetime

# source str_time_prop and random_date: Boris V; Tom Alsberg,
# https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates


def str_time_prop(start, end, time_format, prop):
    """
    Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    """Takes two dates and a random float as input. Returns a random date between the two dates."""
    return str_time_prop(start, end, '%Y-%m-%d', prop)


def get_random_dates(start, end, amount):
    """
    Takes two dates (date time) in the following format: '%Y-%m-%d' and an amount as input. Chooses the specified amount
    of dates randomly. All dates have to be between the two specified dates and no two dates can be the same.

    !! Be careful! if you specify an amount that is higher than the amount of days between your two dates, this function
    will result in an endless loop. !!
    """
    dates = []
    while amount != 0:
        a_random_date = random_date(start, end, random.random())
        date_time_obj = datetime.strptime(a_random_date, '%Y-%m-%d')
        if not date_time_obj in dates:
            dates.append(date_time_obj)
            amount -= 1
    print(dates)
    return dates


if __name__ == '__main__':
    print(random_date("2008-1-1", "2009-1-1", random.random()))
