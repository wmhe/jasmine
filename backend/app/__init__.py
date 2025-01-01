import uuid
from flask import Flask
from flask_cors import CORS

from app.event import EventMapper

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
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

from app import routes