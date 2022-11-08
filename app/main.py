import threading
from concurrent.futures import ThreadPoolExecutor

from flask import Flask

from app.comments.api import comment_blueprint
from app.reports_multiple_applications.service import worker_fn
from app.users.api import user_blueprint
from app.reports.api import report_blueprint
from app.reports_multiple_applications.api import multi_report_blueprint
from config import debug, max_threads
from db import get_database, get_sync_database

db = get_database()
db_sync = get_sync_database()


def create_app():
    flask_app = Flask(__name__)
    flask_app.register_blueprint(comment_blueprint)
    flask_app.register_blueprint(user_blueprint)
    flask_app.register_blueprint(report_blueprint)
    flask_app.register_blueprint(multi_report_blueprint)
    for _ in range(0, max_threads):
        threading.Thread(target=worker_fn).start()
    return flask_app


app = create_app()
if __name__ == "__main__":
    app.run(debug=debug)
