def get_frequency(a_list):
    """
    Takes a list as input. Counts how many times each element occurs and returns each unique element in a dict together
    with the count. (dict) {:int}
    """
    result = dict()
    for item in a_list:
        try:
            result[item] += 1
        except KeyError:
            result[item] = 1
    return result


def highest_counts(frequency_dict, amount):
    """"""
    product_amount = len(frequency_dict)
    most_frequent_items = list()

    product_counts_list = list(frequency_dict.items())
    counts = [item[1] for item in product_counts_list]

    if amount > product_amount:
        amount = product_amount

    while amount:
        highest_count = max(counts)
        index = counts.index(highest_count)
        most_frequent_items.append(product_counts_list[index][0])
        del counts[index]
        del product_counts_list[index]
        amount -= 1

    return most_frequent_items
