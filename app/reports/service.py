import asyncio
from abc import abstractmethod

from app.main import db


collection_name = db["comments"]


class Report:
    @abstractmethod
    async def generate_reports(self) -> None:
        pass

    @abstractmethod
    def getReportName(self):
        pass


class TopFiveCommenters(Report):
    async def generate_reports(self) -> None:
        stage_group_comment = {
            "$group": {
                "_id": "$name",
                "comment_count": {"$sum": 1},
            }
        }
        pipeline = [stage_group_comment]
        results = collection_name.aggregate(pipeline)
        await asyncio.sleep(5)
        return results


    def getReportName(self):
        return "Top Five Commenters"
