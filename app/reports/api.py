import asyncio
import json

from bson.json_util import dumps
from flask import request, make_response, Blueprint

from app.util import list_of_reports

report_blueprint = Blueprint("report", __name__, url_prefix='/reports')


@report_blueprint.route('/', methods=['POST'])
async def report_generator():
    report_name = request.json["report_name"]
    report_obj = list_of_reports[report_name]
    report_obj.insert_report_status(report_name, 'pending')
    reports_ = asyncio.create_task(report_obj.generate_reports())
    await reports_
    report_obj.insert_report_status(report_name, 'done')
    print(type(reports_.result()))
    response = make_response(dumps(reports_.result()), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@report_blueprint.route('/status', methods=['POST'])
async def report_status():
    report_name = request.json["report_name"]
    report_obj = list_of_reports[report_name]
    status = report_obj.get_report_status({'name': str(report_name)})
    response = make_response(json.dumps(status), 200)
    response.headers["Content-Type"] = "application/json"
    return response
