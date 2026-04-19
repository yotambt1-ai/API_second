from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound, BadRequest
import uuid
from models import * 
tasks_bp = Blueprint('tasks_bp', __name__)




@tasks_bp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to my Task API"})

@tasks_bp.route("/tasks", methods=["GET"])
def manage_tasks():
    return jsonify(tasks)

@tasks_bp.route("/tasks/<task_id>", methods=["GET"])
def get_id(task_id):
    for i in tasks:
        if i["id"] == task_id:
            return jsonify(i)
    raise NotFound(f"task {task_id} not found")

@tasks_bp.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    if not data or "title" not in data:
        raise BadRequest("you need to create a title")
    
    new_task = {
        "id": str(uuid.uuid4()),
        "title": data.get("title"),
        "completed": False,
    }    
    tasks.append(new_task)
    return jsonify(new_task), 201

@tasks_bp.route("/tasks/<task_id>", methods=["PUT"])
def put_task(task_id):
    data = request.get_json()
    
    if not data:
        raise BadRequest("Missing data for update")

    for i in tasks: 
        if i["id"] == task_id:
            i["title"] = data.get("title", i["title"])
            i["completed"] = data.get("completed", i["completed"])
            return jsonify(i), 200
            
    raise NotFound(f"Cannot update: task {task_id} not found")