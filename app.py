from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# タスクモデル（データベース構造）
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    assignee = db.Column(db.String(100), nullable=False)
    progress = db.Column(db.Integer, nullable=False, default=0)

# データベースを初期化
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    name = request.form.get("name")
    deadline = datetime.strptime(request.form.get("deadline"), '%Y-%m-%d')
    department = request.form.get("department")
    assignee = request.form.get("assignee")
    progress = request.form.get("progress")

    new_task = Task(name=name, deadline=deadline, department=department, assignee=assignee, progress=int(progress))
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    task = Task.query.get(task_id)
    task.progress = int(request.form.get("progress"))
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
