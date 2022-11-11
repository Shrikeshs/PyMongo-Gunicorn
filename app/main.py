import json
import logging
import signal
import threading
import time

from flask import Flask, make_response

from app.comments.api import comment_blueprint
from app.reports_multiple_applications.service import BackGroundWorker, worker_fne
from app.users.api import user_blueprint
from app.reports.api import report_blueprint
from app.reports_multiple_applications.api import multi_report_blueprint
from config import debug, max_threads
from db import get_database, get_sync_database

db = get_database()
db_sync = get_sync_database()
keep_loop_running = True
stop_event = threading.Event()


def create_app():
    global keep_loop_running
    flask_app = Flask(__name__)
    flask_app.register_blueprint(comment_blueprint)
    flask_app.register_blueprint(user_blueprint)
    flask_app.register_blueprint(report_blueprint)
    flask_app.register_blueprint(multi_report_blueprint)

    for _ in range(0, max_threads):
        threading_thread = threading.Thread(target=worker_fne, args=(stop_event,))
        threading_thread.start()
    return flask_app


app = create_app()


@app.route("/shutdown", methods=["POST"])
def shutdown_threads():
    stop_event.set()
    logging.info("Shutting Down background threads..")
    response = make_response(json.dumps({"message": "The Worker threads have been shut down"}), 200)
    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == "__main__":
    app.run(debug=debug)
