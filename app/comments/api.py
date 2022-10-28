import json

from bson import ObjectId
from flask import request, Blueprint, jsonify, abort, make_response



comment_blueprint = Blueprint("comment", __name__, url_prefix='/comments')


@comment_blueprint.route('/', methods=['POST'])
def create_comments():
    request_json = request.json
    if request_json is None or len(request_json) == 0:
        abort(400, description="The Incoming Request if empty")
    request_json["movie_id"] = ObjectId(request_json.get("movie_id"))
    from app.comments.service import db_create_comment, db_query_comments
    id_inserted = db_create_comment(request_json)
    items = db_query_comments({'_id': ObjectId(id_inserted.inserted_id)})
    response = make_response(json.dumps(items), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@comment_blueprint.route('/<id>', methods=['DELETE'])
def delete_comment(id):
    id_to_delete = id
    if id_to_delete is None:
        abort(400, description="The id to delete cannot be empty")
    from app.comments.service import db_delete_comment
    db_delete_comment(id_to_delete)
    response = make_response("Deleted", 204)
    response.headers["Content-Type"] = "application/json"
    return response


@comment_blueprint.route('/', methods=['GET'])
def query_comments():
    request_args = request.args
    from app.comments.service import db_query_comments
    items = db_query_comments(request_args)
    response = make_response(json.dumps(items), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@comment_blueprint.route('/<id>', methods=['PATCH'])
def update_comment(id):
    from app.comments.service import db_update_comment, db_query_comments
    db_update_comment(request, id)
    items = db_query_comments({'_id': ObjectId(id)})
    response = make_response(json.dumps(items), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@comment_blueprint.route('/<id>', methods=['PUT'])
def update_comment_put(id):
    from app.comments.service import db_update_comment, db_query_comments
    db_update_comment(request, id)
    items = db_query_comments({'_id': ObjectId(id)})
    response = make_response(json.dumps(items), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@comment_blueprint.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400
