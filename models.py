
import uuid
from db import db
tasks = [
    {"id": "1", "title":"Learn Flask", "is_completed": False},
    {"id": "2", "title":"Build API", "is_completed": False},
    {"id": "3", "title":"Test with Postman", "is_completed": True}
]

def get_all_tasks():
    return tasks

def get_task_by_id(task_id):
    for task in tasks:
        if task["id"] == task_id:
           return list(db.tasks.find())
        
def create_task(task_data):
    new_task = {
        "id": uuid.uuid4(),
        "title": task_data['title'],
        "is_completed": False
    }
    db.tasks.insert_one(new_task)
    return new_task