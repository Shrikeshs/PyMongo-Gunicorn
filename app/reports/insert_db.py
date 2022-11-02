from bson import ObjectId

from app.reports.service import TopKReporters


def get_report_status(request_json):
    from app.main import db_sync
    report_collection = db_sync["report_status"]
    find = report_collection.find(request_json)
    result = []
    for doc in find:
        result.append(doc)
    return result


def insert_report_status(report_name, status, response):
    from app.main import db_sync
    report_collection = db_sync["report_status"]
    request_json = {"name": report_name, "status": status, "response": response}
    id_inserted = report_collection.insert_one(request_json)
    return id_inserted


def update_report(_id, status, result):
    from app.main import db
    report_collection = db["report_status"]
    filter_for_id = {'_id': ObjectId(_id)}
    cond_dict = TopKReporters().build_cond_dict({"status": status, "response": result})
    new_value = {"$set": cond_dict}
    report_collection.update_one(filter_for_id, new_value)
