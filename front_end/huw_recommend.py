from flask import Flask
from flask_restful import Api, Resource
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from recommendation_engines.bought_together import recommend as bought_together
import recommendation_engines.trending_products.recommend as trending
import recommendation_engines.popular_months.recommend as date_filtering

app = Flask(__name__)
api = Api(app)

# We define these variables to (optionally) connect to an external MongoDB
# instance.
envvals = ["MONGODBUSER","MONGODBPASSWORD","MONGODBSERVER"]
dbstring = 'mongodb+srv://{0}:{1}@{2}/test?retryWrites=true&w=majority'

# Since we are asked to pass a class rather than an instance of the class to the
# add_resource method, we open the connection to the database outside of the
# Recom class.
load_dotenv()
if os.getenv(envvals[0]) is not None:
    envvals = list(map(lambda x: str(os.getenv(x)), envvals))
    client = MongoClient(dbstring.format(*envvals))
else:
    client = MongoClient()
database = client.huwebshop


class Recom(Resource):
    """ This class represents the REST API that provides the recommendations for
    the webshop. At the moment, the API simply returns a random set of products
    to recommend."""

    def get(self, profileid, count):
        """ This function represents the handler for GET requests coming in
        through the API. It currently returns a random sample of products. """
        print(profileid, count)
        profile_id, page_type, product_id = tuple(profileid.split(sep='.'))
        if str(page_type) == 'product':
            return bought_together.recommending(product_id, count), 200
        if str(page_type) == 'category':
            return date_filtering.recommending(count), 200
        if str(page_type) == 'shoppingcart':
            return date_filtering.recommending(count), 200
        return None, 400


# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
api.add_resource(Recom, "/<string:profileid>/<int:count>")


if __name__ == '__main__':
    app.run(debug=True, port=5001)
