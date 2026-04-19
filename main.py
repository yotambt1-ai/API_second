from flask import Flask
from routs import tasks_bp
from erors import errors_bp
from pymongo import MongoClient
app = Flask(__name__)

app.register_blueprint(tasks_bp)
app.register_blueprint(errors_bp)
if __name__ == "__main__":
    app.run(debug=True, port=5001)