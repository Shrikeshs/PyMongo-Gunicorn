from bson import json_util
from flask import Blueprint, request, abort, jsonify, make_response

from app.models import Users

user_blueprint = Blueprint("user", __name__, url_prefix='/users')


@user_blueprint.route('/', methods=['POST'])
def create_users():
    request_json = request.json
    if request_json is None or len(request_json) == 0:
        abort(400, description="The Incoming Request if empty")
    from app.users.service import db_create_comment
    id_inserted = db_create_comment(request_json)
    response = make_response('Id inserted Successfully : ' + str(id_inserted.inserted_id), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@user_blueprint.route('/<id>', methods=['DELETE'])
def delete_user():
    id_to_delete = request.args["id"]
    if id_to_delete is None:
        abort(400, description="The id to delete cannot be empty")
    from app.users.service import db_delete_comment
    db_delete_comment(id_to_delete)
    response = make_response('Id inserted Successfully : ' + str(id_to_delete), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@user_blueprint.route('/', methods=['GET'])
def list_users():
    from app.users.service import db_list_comments
    items = db_list_comments()
    response = make_response(items, 200)
    response.headers["Content-Type"] = "application/json"
    return response


@user_blueprint.route('/', methods=['POST'])
def query_users():
    from app.users.service import db_query_comments
    items = db_query_comments(request.json)
    return json_util.dumps(items)


@user_blueprint.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400


def build_user_item(item):
    user = Users(str(item["_id"]),
                 str(item["name"]),
                 str(item["email"]),
                 str(item["password"]))
    return user
