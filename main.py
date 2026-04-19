from flask import Flask, render_template  
import os
from dotenv import load_dotenv
from db import mongo, init_db #
from routs import tasks_bp 

load_dotenv()

app = Flask(__name__)

init_db(app)

app.register_blueprint(tasks_bp, url_prefix='/tasks')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)