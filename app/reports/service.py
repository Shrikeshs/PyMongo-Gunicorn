import asyncio
from abc import abstractmethod
from typing import Any

from app.main import db

collection_name = db["comments"]


class Report:
    @abstractmethod
    async def generate_reports(self) -> list[Any]:
        pass

    @abstractmethod
    def get_report_name(self) -> str:
        pass


class TopFiveCommenters(Report):
    async def generate_reports(self) -> list[Any]:
        stage_group_comment = {
            "$group": {
                "_id": "$name",
                "comment_count": {"$sum": 1},
            }
        }
        sort = {"$sort": {"comment_count": -1}}
        limit = {"$limit": 5}
        pipeline = [stage_group_comment, sort, limit]
        await asyncio.sleep(5)
        result = []
        async for doc in collection_name.aggregate(pipeline):
            result.append(doc)
        return result

    def get_report_name(self):
        return "Top Five Commenters"

    def get_report_status(self, report_name):
        report_collection = db["report_status"]
        response = self.build_response(report_collection.find(report_name))
        return response

    def insert_report_status(self, report_name, status):
        report_collection = db["report_status"]
        request_json = {"name": report_name, "status": status}
        id_inserted = report_collection.insert_one(request_json)
        return id_inserted

    def build_response(self, items):
        results = {}
        for item in items:
            results["_id"] = str(item.get("_id"))
            results["name"] = str(item.get("name"))
            results["status"] = str(item.get("status"))
            results["result"] = str(item.get("result"))
        return results
