def get_daily_bar(total_traffic):
    """
    Takes a list with 12 count values. Each value represents the amount of hits a given product has ever received in
    a month.
    Calculates the minimum amount of hits a product has to receive any given week for that traffic to be significantly
    higher. (140 % + 50)
    """
    average_traffic = total_traffic / 52
    return (average_traffic * 1.4) + 50


def get_overall_bar(traffic_per_month):
    """
    Takes a list with 12 count values. Each value represents the amount of hits a given product has ever received in
    during a month. Calculates the minimum amount of hits a product has to receive any given month for that traffic to
    be significantly higher. (140 % + 50)
    """
    average_traffic = sum(traffic_per_month) / 12
    return average_traffic * 1.4 + 50