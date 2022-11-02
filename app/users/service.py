from bson import ObjectId
from app.util import db

collection_name = db["users"]


def db_create_comment(request_json):
    id_inserted = collection_name.insert_one(request_json)
    return id_inserted


def db_delete_comment(id_to_delete):
    collection_name.delete_one({'_id': ObjectId(id_to_delete)})


def db_list_comments():
    return collection_name.find()


def db_query_comments(request_json):
    items = collection_name.find(request_json)
    return items


def db_update_comment(filter_for_id, new_value):
    collection_name.update_one(filter_for_id, new_value)
