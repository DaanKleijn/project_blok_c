def difference(product_1_properties, product_2_properties):
    count = 0
    for a_property in product_1_properties:
        if a_property not in product_2_properties:
            count += 1
    return count




