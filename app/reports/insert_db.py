import logging

from bson import ObjectId

from app.reports.service import TopKReporters


def build_response(result):
    for res in result:
        res["_id"] = str(res["_id"])
    return result


def get_report_status(request_json):
    """
       Endpoint for report generation

       Parameters:
           str1 (str):The string which is to be reversed.

       Returns:
           reverse(str1):The string which gets reversed.
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
       Endpoint for report generation

       Parameters:
           str1 (str):The string which is to be reversed.

       Returns:
           reverse(str1):The string which gets reversed.
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
       Endpoint for report generation

       Parameters:
           str1 (str):The string which is to be reversed.

       Returns:
           reverse(str1):The string which gets reversed.
       """
    from app.main import db
    report_collection = db["report_status"]
    filter_for_id = {'_id': ObjectId(_id)}
    cond_dict = TopKReporters().build_cond_dict({"status": status, "response": result})
    new_value = {"$set": cond_dict}
    logging.info('Updating report with id -> ' + str(filter_for_id))
    report_collection.update_one(filter_for_id, new_value)
