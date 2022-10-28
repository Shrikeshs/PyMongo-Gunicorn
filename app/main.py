from flask import Flask

from app.comments.api import comment_blueprint

from app.users.api import user_blueprint
from app.reports.api import report_blueprint
from db import get_database
from config import debug

db = get_database()


def create_app():
    flask_app = Flask(__name__)
    flask_app.register_blueprint(comment_blueprint)
    flask_app.register_blueprint(user_blueprint)
    flask_app.register_blueprint(report_blueprint)
    return flask_app


app = create_app()
if __name__ == "__main__":
    app.run(debug=debug)
