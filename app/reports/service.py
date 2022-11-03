from abc import abstractmethod
from typing import Any


class Report:
    @abstractmethod
    async def generate_reports(self, k=str, id=str) -> list[Any]:
        pass

    @abstractmethod
    def get_report_name(self) -> str:
        pass


class TopKReporters(Report):

    async def generate_reports(self, k=str, _id=str) -> list[Any]:
        """
           Implemented fn to generate reports

           Parameters:
               _id (str): The report id that is being generated
               k (str): The top 'k' commenters to generate
           Returns:
               result(list):The result of the report
           """
        from app.main import db
        from app.reports.insert_db import update_report
        collection_name = db["comments"]
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
        async for doc in aggregate:
            result.append(doc)
        update_report(_id, 'done', result)
        return result

    def get_report_name(self):
        """
           Fn to generate report name

           Parameters:
               str1 (str):The string which is to be reversed.

           Returns:
               reverse(str1):The string which gets reversed.
           """
        return "top_commentors"

    @staticmethod
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

    @staticmethod
    def build_response(items):
        results = {}
        for item in items:
            results["_id"] = str(item.get("_id"))
            results["name"] = str(item.get("name"))
            results["status"] = str(item.get("status"))
            results["response"] = str(item.get("response"))
        return results
