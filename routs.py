from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound, BadRequest
import uuid
from db import mongo  

tasks_bp = Blueprint('tasks_bp', __name__)

@tasks_bp.route("/", methods=["GET"])
def get_all_tasks():
    tasks_from_db = list(mongo.db.tasks.find())
    for task in tasks_from_db:
        task['_id'] = str(task['_id'])
    return jsonify(tasks_from_db)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task_by_id(task_id):
    task = mongo.db.tasks.find_one({"id": task_id})
    if not task:
        raise NotFound(f"task {task_id} not found")
    task['_id'] = str(task['_id'])
    return jsonify(task)

@tasks_bp.route("/", methods=["POST"])
def add_task():
    data = request.get_json()
    if not data or "title" not in data:
        raise BadRequest("you need to create a title")
    
    new_task = {
        "id": str(uuid.uuid4()),
        "title": data.get("title"),
        "completed": False,
    }    
    
    mongo.db.tasks.insert_one(new_task)
    new_task.pop('_id', None)
    return jsonify(new_task), 201

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    if not data:
        raise BadRequest("Missing data for update")

    # אם התקבלה בקשה לעדכן את המשימה כהושלמה, נמחק אותה לגמרי
    if data.get("completed") is True:
        result = mongo.db.tasks.delete_one({"id": task_id})
        if result.deleted_count == 0:
            raise NotFound(f"task {task_id} not found")
        return jsonify({"message": "task deleted"}), 200

    update_fields = {}
    if "title" in data:
        update_fields["title"] = data["title"]
    if "completed" in data:
        update_fields["completed"] = data["completed"]

    result = mongo.db.tasks.update_one(
        {"id": task_id}, 
        {"$set": update_fields}
    )

    if result.matched_count == 0:
        raise NotFound(f"task {task_id} not found")
    
    return jsonify({"message": "task updated successfully"}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    result = mongo.db.tasks.delete_one({"id": task_id})
    if result.deleted_count == 0:
        raise NotFound(f"task {task_id} not found")
    return jsonify({"message": "task deleted"}), 200