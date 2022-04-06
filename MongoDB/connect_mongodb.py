import pymongo


def connect():
    """Connects to the local MongoDB database."""
    # connect to database
    client = pymongo.MongoClient()
    # open database
    db = client.huwebshop
    # open collections
    return db
