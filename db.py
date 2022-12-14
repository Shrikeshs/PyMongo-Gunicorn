import certifi
import motor.motor_asyncio
import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from config import mongo_connection_url, db_name


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = mongo_connection_url

    # Create a connection using MongoClient
    client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING, tlsCAFile=certifi.where(), connect=False)
    # Return the Database of our interest
    return client[db_name]


def get_sync_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = mongo_connection_url
    try:
        # Create a connection using MongoClient
        client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where(), connect=False)
    except ConnectionFailure as e:
        print("Could not connect to server: %s" % e)
        return None
    # Return the Database of our interest
    return client[db_name]


db = get_database()
db_sync = get_sync_database()
