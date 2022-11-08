import pymongo
from bson import ObjectId

from app.models import ResponseMetadata, PaginatedResponse
from app.main import db_sync

collection_name = db_sync["users"]


def db_create_comment(request_json):
    id_inserted = collection_name.insert_one(request_json)
    return id_inserted


def db_delete_comment(id_to_delete):
    collection_name.delete_one({'_id': ObjectId(id_to_delete)})


def db_list_comments():
    return collection_name.find()


def db_query_users_with_cursor(limit, next_id, sort_by, sort_order):
    collection = db_sync["users"]
    items = get_cursor_paginated_response(collection, limit, next_id,
                                          sort_by, sort_order)
    return items


def convert_id(item):
    item["_id"] = str(item["_id"])


def get_sort_order(sort_order):
    if str(sort_order) == 'ASC':
        return pymongo.ASCENDING
    return pymongo.DESCENDING


def get_cursor_paginated_response(collection, limit, next_id, sort_by, sort_order):
    metadata = ResponseMetadata()
    order = get_sort_order(sort_order)
    if next_id:
        request_for_next_id = {"_id": {"$lt": ObjectId(next_id)}}
        items = collection.find(request_for_next_id).sort([(str(sort_by), order), ("_id", order)]).limit(limit)
    else:
        items = collection.find().sort([(str(sort_by), order), ("_id", order)]).limit(limit)
    results = []
    for item in items:
        convert_id(item)
        results.append(item)
    if len(results):
        cur_last_id = results[-1]["_id"]
        cur_first_id = results[0]["_id"]
        last_name_req = {"_id": {"$lt": ObjectId(cur_last_id)}}
        last_name_db_result = collection.find_one(last_name_req)
        if last_name_db_result:
            metadata.has_next = True
            metadata.next = cur_last_id
        first_name_req = {"_id": {"$gt": ObjectId(cur_first_id)}}
        first_name_db_result = collection.find_one(first_name_req)
        if first_name_db_result:
            metadata.has_previous = True
            metadata.previous = cur_first_id
    return PaginatedResponse(results, metadata.__dict__)


def db_query_comments(request_json):
    items = collection_name.find(request_json)
    return items


def db_update_comment(filter_for_id, new_value):
    collection_name.update_one(filter_for_id, new_value)
