import asyncio
import logging
import threading

from bson import ObjectId
from bson.json_util import dumps
from flask import request, make_response, Blueprint, abort
from app.reports.insert_db import insert_report_status, get_report_status
from app.util import list_of_reports

report_blueprint = Blueprint("report", __name__, url_prefix='/reports')

work_queue = asyncio.Queue(5)


@report_blueprint.route('/', methods=['POST'])
async def report_generator():
    if work_queue.full():
        logging.debug('Worker is full...')
        abort(400, description="Worker is full, please try after sometime")
    report_name = request.json["report_name"]
    request_args = request.args
    k = request_args["k"]
    report_obj = list_of_reports[report_name]
    from app.util import loop
    report_status_task = insert_report_status(report_name, 'pending', [])
    logging.info('Report has been inserted to MongoDb')
    reports_task = loop.create_task(report_obj.generate_reports(k, report_status_task.inserted_id))
    work_queue.put_nowait(reports_task)
    response = make_response(dumps(report_status_task.inserted_id), 202)
    response.headers["Content-Type"] = "application/json"
    return response


async def worker_fn():
    while not work_queue.empty():
        task = await work_queue.get()
        await task
        work_queue.task_done()


def run_periodically():
    from app.util import loop
    loop.run_until_complete(loop.create_task(worker_fn()))
    threading.Timer(10, run_periodically).start()


run_periodically()


@report_blueprint.route('/<id>', methods=['POST'])
def report_status(id):
    report_name = request.json["report_name"]
    logging.info('Retrieving report for id : ' + str(id))
    id_ = get_report_status({'name': str(report_name), "_id": ObjectId(id)})
    response = make_response(dumps(id_), 200)
    response.headers["Content-Type"] = "application/json"
    return response
