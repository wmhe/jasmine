import uuid

from .event import EventMapper
from flask import Blueprint

bp = Blueprint("api", __name__)

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
from app.api import errors, tokens, users, events
