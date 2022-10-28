import asyncio
import json
import time
from asyncio import tasks

from bson.json_util import dumps
from flask import request, make_response, Blueprint

from app.models import Response

report_blueprint = Blueprint("report", __name__, url_prefix='/reports')


@report_blueprint.route('/', methods=['POST'])
async def report_generator():
    start = time.perf_counter()
    request_json = request.json
    report_name = request_json["report_name"]
    from app.reports.service import TopFiveCommenters
    reports_ = asyncio.create_task(TopFiveCommenters().generate_reports())
    await reports_
    end = time.perf_counter()
    if reports_.done():
        response = make_response(dumps(reports_.result()), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    print(end - start)
    response_obj = Response(TopFiveCommenters().getReportName(), "PENDING", str(time.time()))
    response = make_response(json.dumps(response_obj.__dict__), 200)
    response.headers["Content-Type"] = "application/json"
    return response
