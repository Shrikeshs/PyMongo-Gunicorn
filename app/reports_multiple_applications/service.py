import atexit
import logging
import threading
import time
from typing import Any

from bson import ObjectId
from pymongo import ReturnDocument


from app.reports.insert_db import get_enqueue_tasks

keep_running = True


def generate_reports(k=int, _id=str) -> list[Any]:
    """
       Implemented fn to generate reports

       Parameters:
           _id (str): The report id that is being generated
           k (int): The top 'k' commenters to generate
       Returns:
           result(list):The result of the report

       """
    from app.main import db_sync
    collection_name = db_sync["comments"]
    stage_group_comment = {
        "$group": {
            "_id": "$name",
            "comment_count": {"$sum": 1},
        }
    }
    sort = {"$sort": {"comment_count": -1}}
    limit_number = int(k)
    limit = {"$limit": limit_number}
    pipeline = [stage_group_comment, sort, limit]
    result = []

    aggregate = collection_name.aggregate(pipeline)
    for doc in aggregate:
        result.append(doc)
    return result


def insert_report_status(report_name, status, response, request_json):
    """
        Db service fn to insert the report status

       Parameters:
           report_name (str):The report name that is to be generated.
           status (str):The status of the report.
           response (list):The response list containing the report results.
           request_json(dict)
       Returns:
            Json response of the report status structured as follows
            _id = id of report
            name = name of the required report
            status = status of the report (pending or done)
            response = if status = done, we add the list of results to this else []
       """
    from app.main import db_sync
    k = request_json["k"]
    report_collection = db_sync["report_status"]
    request_json = {"name": report_name, "status": status, "response": response, "k": int(k)}
    id_inserted = report_collection.insert_one(request_json)
    logging.info('Id has been inserted to MongoDb -> ' + str(id_inserted.inserted_id))
    result = {"_id": str(id_inserted.inserted_id)}
    return result


def update_report(_id, status, result):
    """
      Db service fn for updating report with response and status update.

       Parameters:
           _id (str):The string which is to be reversed.
           status (str):The status of the report.
           result (list):The response list containing the report results.
    """
    from app.main import db_sync
    report_collection = db_sync["report_status"]
    filter_for_id = {'_id': ObjectId(_id)}
    cond_dict = build_cond_dict({"status": status, "response": result})
    logging.info('Updating report with id -> ' + str(filter_for_id))
    report_collection.find_one_and_update({'_id': ObjectId(_id)},
                                          {"$set": cond_dict},
                                          return_document=ReturnDocument.AFTER)


def build_cond_dict(json):
    """
       fn to build result dictionary

       Parameters:
           json (dict):The dict containing the report_status response from MongoDb

       Returns:
           reverse(str1):The string which gets reversed.
    """
    status = json.get("status")
    response = json.get("response")
    cond_dict = {}
    if status is not None:
        cond_dict['status'] = status
    if response is not None:
        cond_dict['response'] = response
    return cond_dict


def exit_handler():
    print('My application is ending!')


def worker_fn(keep_loop_running):
    """
       Consumer fn to consume the worker queue in mongo db with tasks
    """
    while keep_loop_running:
        try:
            db_report_task = get_enqueue_tasks()
            if db_report_task is not None:
                logging.info(f"Thread {threading.currentThread().getName()} is picking up db task with _id {db_report_task['_id']}")
                logging.info("Processing Task, report_id : " + str(db_report_task["_id"]))
                k = db_report_task["k"]
                reports = generate_reports(k, db_report_task["_id"])
                update_report(db_report_task["_id"], 'done', reports)
        except RuntimeError as e:
            logging.info("RunTime exception raised while running threads in the background " + str(e))
    logging.info("The background threads have been stopped...")
