import logging

from bson import ObjectId

from app.reports.service import TopKReporters


def build_response(result):
    for res in result:
        res["_id"] = str(res["_id"])
    return result


def get_report_status(request_json):
    """
       Db service fn to get status report from report_status collection
       from MongoDB

       Parameters:
           request_json (dict):The json which contains the filters to find the report

       Returns:
           result: report status that is to be returned
       """
    from app.main import db_sync
    report_collection = db_sync["report_status"]
    find = report_collection.find(request_json)
    result = []
    for doc in find:
        result.append(doc)
    build_response(result)
    return result


def insert_report_status(report_name, status, response):
    """
        Db service fn to insert the report status

       Parameters:
           report_name (str):The report name that is to be generated.
           status (str):The status of the report.
           response (list):The response list containing the report results.

       Returns:
            Json response of the report status structured as follows
            _id = id of report
            name = name of the required report
            status = status of the report (pending or done)
            response = if status = done, we add the list of results to this else []
       """
    from app.main import db_sync
    report_collection = db_sync["report_status"]
    request_json = {"name": report_name, "status": status, "response": response}
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
    from app.main import db
    report_collection = db["report_status"]
    filter_for_id = {'_id': ObjectId(_id)}
    cond_dict = TopKReporters().build_cond_dict({"status": status, "response": result})
    new_value = {"$set": cond_dict}
    logging.info('Updating report with id -> ' + str(filter_for_id))
    report_collection.update_one(filter_for_id, new_value)


def insert_report_tasks(report_name, _id):
    from app.main import db_sync
    report_collection = db_sync["report_tasks"]
    request_json = {"name": report_name, "report_id": _id, "status": "enqueued"}
    id_inserted = report_collection.insert_one(request_json)
    return id_inserted.inserted_id


def get_enqueue_tasks():
    from app.main import db_sync
    report_collection = db_sync["report_tasks"]
    filter_for_id = {'status': "enqueued"}
    find = report_collection.find(filter_for_id)
    results = []
    for doc in find:
        results.append(doc)
    if len(results):
        return results
    return None


def update_report_tasks(_id):
    from app.main import db_sync
    report_collection = db_sync["report_tasks"]
    filter_for_id = {'_id': ObjectId(_id)}
    cond_dict = {"status": "done"}
    new_value = {"$set": cond_dict}
    report_collection.update_one(filter_for_id, new_value)
