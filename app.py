from flask import Flask, request, jsonify, render_template, send_file, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from config import Config
from datetime import datetime
import numpy as np
import pandas as pd

# ---------------- APP INIT ----------------
app = Flask(__name__)
app.secret_key = "smart_task_secret_key"
app.config.from_object(Config)

# 🔥 IMPORTANT: session stability fix
app.config['SESSION_COOKIE_SAMESITE'] = "Lax"
app.config['SESSION_COOKIE_SECURE'] = False

db = SQLAlchemy(app)

# ---------------- SOCKET IO ----------------
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# ---------------- MODELS ----------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return redirect('/login-page')

# ---------------- REGISTER ----------------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email exists"}), 400

    user = User(username=username, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registered"})

# ---------------- LOGIN (FIXED) ----------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email, password=password).first()

    if user:
        # 🔥 SESSION FIX (THIS WAS MISSING BEFORE)
        session['user_id'] = user.id
        session['username'] = user.username

        return jsonify({
            "message": "Login successful",
            "user_id": user.id,
            "username": user.username
        })

    return jsonify({"message": "Invalid credentials"}), 401

# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login-page')

    return render_template('dashboard.html')


# ---------------- LOGIN / REGISTER PAGES ----------------
@app.route('/login-page')
def login_page():
    return render_template('login.html')


@app.route('/register-page')
def register_page():
    return render_template('register.html')

# ---------------- TASK APIs ----------------

@app.route('/tasks/<int:user_id>')
def get_tasks(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()

    return jsonify([{
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "priority": t.priority,
        "status": t.status
    } for t in tasks])

# ---------------- ADD TASK ----------------
@app.route('/add-task', methods=['POST'])
def add_task():
    data = request.get_json()

    task = Task(
        title=data['title'],
        description=data['description'],
        priority=data['priority'],
        status=data['status'],
        created_date=str(datetime.now()),
        user_id=data['user_id']
    )

    db.session.add(task)
    db.session.commit()

    socketio.emit("task_updated", {
        "action": "created",
        "task_id": task.id
    })

    return jsonify({"message": "Task created"})

# ---------------- UPDATE TASK ----------------
@app.route('/update-task/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    data = request.get_json()

    if not task:
        return jsonify({"message": "Task not found"}), 404

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.priority = data.get('priority', task.priority)
    task.status = data.get('status', task.status)

    db.session.commit()

    socketio.emit("task_updated", {
        "action": "updated",
        "task_id": id
    })

    return jsonify({"message": "Updated"})

# ---------------- DELETE TASK ----------------
@app.route('/delete-task/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)

    if not task:
        return jsonify({"message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    socketio.emit("task_updated", {
        "action": "deleted",
        "task_id": id
    })

    return jsonify({"message": "Deleted"})

# ---------------- ANALYTICS ----------------
@app.route('/task-analytics/<int:user_id>')
def analytics(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()

    statuses = np.array([t.status for t in tasks])

    total = statuses.size if len(statuses) > 0 else 0
    completed = np.sum(statuses == "Completed")
    pending = np.sum(statuses == "Pending")

    completion_rate = (completed / total * 100) if total else 0

    return jsonify({
        "total_tasks": int(total),
        "completed_tasks": int(completed),
        "pending_tasks": int(pending),
        "completion_rate": round(float(completion_rate), 2)
    })

# ---------------- EXPORT ----------------
@app.route('/export-tasks/<int:user_id>')
def export(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()

    df = pd.DataFrame([{
        "Title": t.title,
        "Description": t.description,
        "Priority": t.priority,
        "Status": t.status
    } for t in tasks])

    file = "tasks.csv"
    df.to_csv(file, index=False)

    return send_file(file, as_attachment=True)

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login-page')

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    socketio.run(app, debug=True)
