import asyncio
import json
import time
from asyncio import tasks

from bson.json_util import dumps
from flask import request, make_response, Blueprint


report_blueprint = Blueprint("report", __name__, url_prefix='/reports')


@report_blueprint.route('/', methods=['POST'])
async def report_generator():
    from app.reports.service import TopFiveCommenters
    commenters = TopFiveCommenters()
    request_json = request.json
    report_name = request_json["report_name"]
    commenters.insert_report_status(report_name, 'pending')
    reports_ = asyncio.create_task(commenters.generate_reports())
    await reports_
    if reports_.done():
        commenters.insert_report_status(report_name, 'done')
        response = make_response(dumps(reports_.result()), 200)
        response.headers["Content-Type"] = "application/json"
        return response


@report_blueprint.route('/status', methods=['POST'])
async def report_status():
    request_json = request.json
    report_name = request_json["report_name"]
    from app.reports.service import TopFiveCommenters
    status = TopFiveCommenters().get_report_status({'name': str(report_name)})
    response = make_response(json.dumps(status), 200)
    response.headers["Content-Type"] = "application/json"
    return response
