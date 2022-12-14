import asyncio
import json
import logging
import threading

from bson import ObjectId
from bson.json_util import dumps
from flask import request, make_response, Blueprint
from app.reports.insert_db import insert_report_status, get_report_status, get_enqueue_tasks, \
    update_report_tasks
from app.util import list_of_reports

report_blueprint = Blueprint("report", __name__, url_prefix='/reports')

maxsize = 5
work_queue = asyncio.Queue(maxsize)


@report_blueprint.route('/', methods=['POST'])
async def report_generator():
    """
     Endpoint for report generation
     Returns:
         Json response of the id of the report stored in Mongo Db
     """
    report_name = request.json["report_name"]
    report_obj = list_of_reports[report_name]
    from app.util import loop
    logging.info('Report has been inserted to MongoDb')
    result_dict = insert_report_status(report_name, 'enqueued', [])
    logging.info('Task has been inserted to MongoDb' + str(result_dict["_id"]))
    db_report_tasks = get_enqueue_tasks()
    while not work_queue.full() and len(db_report_tasks):
        db_task = db_report_tasks.pop()
        report_id = db_task.get("report_id")
        reports_task = loop.create_task(report_obj.generate_reports(request.json, report_id))
        work_queue.put_nowait(reports_task)
        update_report_tasks(db_task.get("_id"))
    response = make_response(json.dumps(result_dict), 202)
    response.headers["Content-Type"] = "application/json"
    
    return response


@report_blueprint.route('/<id>', methods=['POST'])
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


async def worker_fn():
    """
       Consumer fn to consume the worker queue with tasks
    """
    while not work_queue.empty():
        task = await work_queue.get()
        await task
        work_queue.task_done()


def run_periodically():
    from app.util import loop
    loop.run_until_complete(loop.create_task(worker_fn()))
    threading.Timer(10, run_periodically).start()


run_periodically()
