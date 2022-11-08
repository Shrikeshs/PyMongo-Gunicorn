from datetime import datetime

import pymongo
from bson import ObjectId

from app.main import db_sync
from app.models import Comments, ResponseMetadata, PaginatedResponse

collection_name = db_sync["comments"]


def db_create_comment(request_json):
    id_inserted = collection_name.insert_one(request_json)
    return id_inserted


def db_delete_comment(id_to_delete):
    collection_name.delete_one({'_id': ObjectId(id_to_delete)})


def db_list_comments():
    return collection_name.find()


def db_query_comments(page_size, page_number):
    size_page_number = page_size * page_number
    if size_page_number == 0:
        skip = 0
        limit = page_size
    else:
        skip = size_page_number
        limit = page_size
    items = collection_name \
        .find().sort("name", pymongo.ASCENDING) \
        .skip(skip).limit(limit)
    results = build_response(items)
    return results


def convert_id(item):
    item["_id"] = str(item["_id"])


def get_cursor_paginated_response(collection, limit, next_id):
    metadata = ResponseMetadata()
    if next_id:
        request_for_next_id = {"_id": {"$lt": next_id}}
        items = collection.find(request_for_next_id).sort("_id", pymongo.DESCENDING).limit(limit)
    else:
        items = collection.find().sort("name", pymongo.DESCENDING).limit(limit)

    results = []
    for item in items:
        convert_id(item)
        results.append(item)
    if len(results):
        cur_last_name = results[-1]["_id"]
        cur_first_name = results[0]["_id"]
        last_name_req = {"_id": {"$lt": cur_last_name}}
        last_name_db_result = collection.find_one(last_name_req)
        if last_name_db_result:
            metadata.has_next = True
            metadata.next = cur_last_name
        first_name_req = {"_id": {"$gt": cur_first_name}}
        first_name_db_result = collection.find_one(first_name_req)
        if first_name_db_result:
            metadata.has_previous = True
            metadata.previous = cur_first_name
    return PaginatedResponse(results, metadata.__dict__)


def db_query_users_with_cursor(limit, next_id):
    from app.main import db_sync
    collection = db_sync["users"]
    items = get_cursor_paginated_response(collection, limit, next_id)
    return items


def db_update_comment(request, comment_id):
    filter_for_id = {'_id': ObjectId(comment_id)}
    cond_dict = build_cond_dict(request.json)
    new_value = {"$set": cond_dict}
    collection_name.update_one(filter_for_id, new_value)


def build_cond_dict(json):
    email = json.get("email")
    name = json.get("name")
    movie_id = json.get("movie_id")
    comment_type = json.get("type")
    cond_dict = {}
    if email is not None:
        cond_dict['email'] = email
    if name is not None:
        cond_dict['name'] = name
    if movie_id is not None:
        cond_dict['movie_id'] = ObjectId(movie_id)
    if comment_type is not None:
        cond_dict['type'] = comment_type
    current_time = datetime.now()
    cond_dict['date'] = current_time
    return cond_dict


def build_comment_item(item):
    comment = Comments(str(item["_id"]),
                       str(item["name"]),
                       str(item["email"]),
                       str(item["movie_id"]),
                       str(item["text"]),
                       str(item["date"]))
    return comment


def build_response(items):
    results_list = []
    for item in items:
        results = {"_id": str(item.get("_id")), "name": str(item.get("name")), "email": str(item.get("email")),
                   "movie_id": str(item.get("movie_id")), "type": str(item.get("type")), "date": str(item.get("date"))}
        results_list.append(results)
    return results_list
