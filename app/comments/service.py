from bson import ObjectId

from app.main import db
from app.models import Comments

collection_name = db["comments"]


def db_create_comment(request_json):
    id_inserted = collection_name.insert_one(request_json)
    return id_inserted


def db_delete_comment(id_to_delete):
    collection_name.delete_one({'_id': ObjectId(id_to_delete)})


def db_list_comments():
    return collection_name.find()


def db_query_comments(request_json):
    items = collection_name.find(request_json)
    results = build_response(items)
    return results


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
    results = {}
    for item in items:
        results["_id"] = str(item.get("_id"))
        results["name"] = str(item.get("name"))
        results["email"] = str(item.get("email"))
        results["movie_id"] = str(item.get("movie_id"))
        results["type"] = str(item.get("type"))
        results["date"] = str(item.get("date"))
    return results
