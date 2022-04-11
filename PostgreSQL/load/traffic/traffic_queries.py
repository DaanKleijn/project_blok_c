def traffic_all_time_query():
    """
    Returns a query to fetch the product_id and the amount of times the product was bought during a given month.
    Format order is: month_value, product_ids"""
    # source: https://stackoverflow.com/questions/50334946/executemany-select-queries-with-psycopg2
    return """SELECT COUNT(ep.product__id), p.product__id 
    FROM event_products ep, sessions s, products p
    WHERE EXTRACT(MONTH FROM s.session_end) = %s
    AND ep.session__id = s.session__id 
    AND ep.product__id = p.product__id
    AND ep.product__id IN ({})
    AND ep.event_type = 'ordered'
    GROUP BY p.product__id;"""


def traffic_all_time_formatted_query(amount_of_values):
    """"""
    return """SELECT COUNT(ep.product__id), p.product__id 
    FROM event_products ep, sessions s, products p
    WHERE EXTRACT(MONTH FROM s.session_end) = %s
    AND ep.session__id = s.session__id 
    AND ep.product__id = p.product__id
    AND ep.product__id IN ({})
    AND ep.event_type = 'ordered'
    GROUP BY p.product__id;""".format(','.join(['%s'] * amount_of_values))


def traffic_day_query():
    """
    Returns all items that were bought with the amount of times it was bought since a given date.
    Format order is: date_value
    """
    # sadly, we can't call the other function and return that formatted, because the two different types of formatting
    # won't work together when they are embedded like that.
    return """SELECT COUNT(ep.product__id), p.product__id 
    FROM event_products ep, sessions s, products p
    WHERE ep.session__id = s.session__id 
    AND p.product__id = ep.product__id
    AND s.session_end >= %s
    AND ep.event_type = 'ordered'
    GROUP BY p.product__id;"""


def traffic_year_query():
    """
    Returns a query to fetch the amount a product is bought and the product_id, ever since a given date, for all given
    products. Format order is: date_value, product_ids
    """
    # source: https://stackoverflow.com/questions/50334946/executemany-select-queries-with-psycopg2
    return """SELECT COUNT(ep.product__id), p.product__id 
    FROM event_products ep, sessions s, products p 
    WHERE s.session_end >=  %s
    AND ep.session__id = s.session__id
    AND ep.product__id = p.product__id
    AND ep.event_type = 'ordered'
    AND ep.product__id IN ({})
    GROUP BY p.product__id;"""


def traffic_year_formatted_query(amount_of_values):
    """"""
    # sadly, we can't call the other function and return that formatted, because the two different types of formatting
    # won't work together when they are embedded like that.
    return """SELECT COUNT(ep.product__id), p.product__id 
    FROM event_products ep, sessions s, products p 
    WHERE s.session_end >=  %s
    AND ep.session__id = s.session__id
    AND ep.product__id = p.product__id
    AND ep.event_type = 'ordered'
    AND ep.product__id IN ({})
    GROUP BY p.product__id;""".format(','.join(['%s'] * amount_of_values))
