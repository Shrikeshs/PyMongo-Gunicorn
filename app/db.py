import certifi
from pymongo import MongoClient

from config import mongo_connection_url, db_name


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = mongo_connection_url

    # Create a connection using MongoClient
    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where(), connect=False)

    # Return the Database of our interest
    return client[db_name]


