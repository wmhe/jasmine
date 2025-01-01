from flask import jsonify, request
from app import app, event_mapper

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