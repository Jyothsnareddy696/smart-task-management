# Smart Task Management System

## Project Overview
This is a simple web-based Task Management System built using Flask.  
It allows users to register, login, and manage their tasks with real-time updates.

---

## Features

- User Registration
- User Login & Logout
- Add Tasks
- Update Tasks
- Delete Tasks
- View All Tasks
- Task Analytics (Total, Completed, Pending, Completion %)
- Real-time Updates using WebSockets
- Export Tasks to CSV (Pandas)

---

## Tech Stack

- Python
- Flask
- PostgreSQL
- SQLAlchemy
- Flask-SocketIO (WebSockets)
- Pandas
- NumPy
- HTML, CSS, JavaScript

---

## Project Setup

### 1. Clone the project

git clone https://github.com/Jyothsnareddy696/smart-task-management.git


---

### 2. Install dependencies

pip install -r requirements.txt


---

### 3. Setup Database (PostgreSQL)

- Create database:

task_manager


- Run schema file:

database/schema.sql


---

### 4. Run the project

python app.py


---

## API Endpoints

- POST /register → Register user  
- POST /login → Login user  
- GET /tasks/<user_id> → Get all tasks  
- POST /add-task → Add task  
- PUT /update-task/<id> → Update task  
- DELETE /delete-task/<id> → Delete task  
- GET /task-analytics/<user_id> → Get analytics  
- GET /export-tasks/<user_id> → Download CSV  

---

## How it works

- Users login and access dashboard
- Tasks can be added, updated, and deleted
- Dashboard updates automatically using WebSockets
- Analytics show task statistics
- Data is stored in PostgreSQL database

---

## Author

Jyothsna
