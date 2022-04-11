def event_product_query():
    """"""
    return """SELECT ep.product__id FROM event_products ep, sessions s, products p 
    WHERE ep.session__id = s.session__id 
    AND ep.product__id = p.product__id
    AND s.session__id in (SELECT session__id FROM event_products WHERE product__id = %s)
    AND ep.event_type = %s
    AND ep.product__id != %s;"""
