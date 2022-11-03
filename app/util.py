import asyncio

from app.reports.service import TopKReporters

list_of_reports = {"top_commentors": TopKReporters()}

loop = asyncio.new_event_loop()
