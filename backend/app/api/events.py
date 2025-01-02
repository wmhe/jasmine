from flask import jsonify, request

from app.api import bp, event_mapper


@bp.route("/events", methods=["GET"])
def get_events() -> None:
    response_object = {"status": "success"}
    response_object["events"] = event_mapper.get_all_events()
    return jsonify(response_object)


@bp.route("/events", methods=["POST"])
def create_event() -> None:
    response_object = {"status": "success"}
    post_data = request.get_json()
    event_mapper.insert(post_data.get("title"), post_data.get("start"))
    response_object["message"] = "Event added"
    return jsonify(response_object)


@bp.route("/events/<int:id>", methods=["PUT"])
def update_event(id) -> None:
    response_object = {"status": "success"}

    post_data = request.get_json()
    event_mapper.update(id, post_data.get("title"), post_data.get("start"))
    response_object["message"] = "Event updated"

    return jsonify(response_object)


@bp.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id) -> None:
    response_object = {"status": "success"}
    event_mapper.delete(id)
    response_object["message"] = "Event deleted"
    return jsonify(response_object)
