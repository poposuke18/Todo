from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# Flaskアプリケーションの設定
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemyのインスタンスを作成
db = SQLAlchemy(app)

migrate = Migrate(app, db)


# タスクモデル（データベース構造）
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    assignee = db.Column(db.String(100), nullable=False)
    progress = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(50), nullable=False, default="Not Started")



# データベースを初期化
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    tasks = Task.query.all()
    now = datetime.now().date()
    return render_template("index.html", tasks=tasks, now=now)

@app.route("/add", methods=["POST"])
def add_task():
    name = request.form.get("name")
    deadline = datetime.strptime(request.form.get("deadline"), '%Y-%m-%d')
    department = request.form.get("department")
    assignee = request.form.get("assignee")
    progress = request.form.get("progress")
    status = request.form.get("status")  # 新しいステータス

    new_task = Task(name=name, deadline=deadline, department=department, assignee=assignee, progress=int(progress), status=status)
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get(task_id)
    if request.method == "POST":
        task.name = request.form.get("name")
        task.deadline = datetime.strptime(request.form.get("deadline"), '%Y-%m-%d')
        task.department = request.form.get("department")
        task.assignee = request.form.get("assignee")
        task.progress = int(request.form.get("progress"))
        task.status = request.form.get("status")  # ステータス更新
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", task=task)


if __name__ == "__main__":
    app.run(debug=True)
