"""Module providing the main entry point for the application."""

import os
import sys
import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS

from .event import EventMapper

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    event_mapper = EventMapper(
        [
            {
                "id": uuid.uuid4().hex,
                "title": "event 1",
                "start": "2024-12-29",
            },
            {
                "id": uuid.uuid4().hex,
                "title": "event 2",
                "start": "2024-12-30",
            },
        ]
    )

    @app.route("/api/v1/events", methods=["GET", "POST"])
    def events() -> None:
        response_object = {"status": "success"}
        if request.method == "POST":
            post_data = request.get_json()
            event_mapper.insert(post_data.get("title"), post_data.get("start"))
            response_object["message"] = "Event added"
        else:
            response_object["events"] = event_mapper.get_all_events()
        return jsonify(response_object)

    @app.route("/api/v1/events/<event_id>", methods=["PUT", "DELETE"])
    def event(event_id) -> None:
        response_object = {"status": "success"}
        if request.method == "PUT":
            post_data = request.get_json()
            event_mapper.update(
                event_id, post_data.get("title"), post_data.get("start")
            )
            response_object["message"] = "Event updated"
        elif request.method == "DELETE":
            event_mapper.delete(event_id)
            response_object["message"] = "Event deleted"
        return jsonify(response_object)

    return app
