import json
import logging

from bson import ObjectId
from bson.json_util import dumps
from flask import request, make_response, Blueprint

from app.reports.insert_db import get_report_status
from app.reports_multiple_applications.service import insert_report_status

multi_report_blueprint = Blueprint("multi_report", __name__, url_prefix='/multi/reports')


@multi_report_blueprint.route('/', methods=['POST'])
def report_generator():
    """
     Endpoint for report generation
     Returns:
         Json response of the id of the report stored in Mongo Db
     """
    report_name = request.json["report_name"]
    logging.info('Report has been inserted to MongoDb')
    result_dict = insert_report_status(report_name, 'enqueued', [], request.json)
    logging.info('Task has been inserted to MongoDb' + str(result_dict["_id"]))
    response = make_response(json.dumps(result_dict), 202)
    response.headers["Content-Type"] = "application/json"
    return response


@multi_report_blueprint.route('/<id>', methods=['POST'])
def report_status(id):
    """
       Endpoint for report result polling

       Parameters:
           id (str):The report id that is to be retrieved

       Returns:
           Json response of the report status structured as follows
            _id = id of report
            name = name of the required report
            status = status of the report (pending or done)
            response = if status = done, we add the list of results to this else []
    """
    report_name = request.json["report_name"]
    logging.info('Retrieving report for id : ' + str(id))
    id_ = get_report_status({'name': str(report_name), "_id": ObjectId(id)})
    response = make_response(dumps(id_), 200)
    response.headers["Content-Type"] = "application/json"
    return response
