from uuid import UUID
import sqlalchemy as sa
from flask import request

from app import db
from app.api import bp
from app.api.errors import bad_request
from app.models import Event


@bp.route("/events", methods=["GET"])
def get_events():
    page = 1
    per_page = min(request.args.get("per_page", 10, type=int), 100)
    return Event.to_collection_dict(sa.select(Event), page, per_page, "api.get_events")


@bp.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    if "title" not in data or "start" not in data:
        return bad_request("must include title and start fields")
    event = Event()
    event.from_dict(data)
    db.session.add(event)
    db.session.commit()
    return event.to_dict(), 201


@bp.route("/events/<id>", methods=["PUT"])
def update_event(id: str):
    event = db.get_or_404(Event, UUID(id))
    data = request.get_json()
    event.from_dict(data)
    db.session.commit()
    return event.to_dict(), 200


@bp.route("/events/<id>", methods=["DELETE"])
def delete_event(id: str):
    event = db.get_or_404(Event, UUID(id))
    db.session.delete(event)
    db.session.commit()
    return {"success": True}, 200
