📌 Smart Task Management System

A full-stack web application built using Flask + PostgreSQL that allows users to register, login, and manage their tasks efficiently with priority and status tracking.

🚀 Features
User registration & login (authentication)
Create, update, delete tasks
Task priority management (Low / Medium / High)
Task status tracking (Pending / Completed)
User-specific task isolation
RESTful API architecture
PostgreSQL database integration

🛠️ Tech Stack
Backend: Python (Flask)
Database: PostgreSQL
Frontend: HTML, CSS, JavaScript
API: REST APIs
Tools: Postman, pgAdmin

📂 Project Structure
smart-task-management/
│
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── routes.py
│   ├── config.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── database/
│   └── schema.sql
│
├── schema.pdf
├── README.md
└── .env.example

⚙️ Installation & Setup
1. Clone Repository
git clone (https://github.com/Jyothsnareddy696/smart-task-management.git)
cd smart-task-management
2. Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
3. Install Dependencies
pip install -r requirements.txt
4. Setup Database (PostgreSQL)
psql -U postgres -f database/schema.sql
5. Run Application
python backend/app.py

🔗 API Endpoints
Auth APIs
POST /api/register → Register user
POST /api/login → Login user
Task APIs
GET /api/tasks → Get all tasks
POST /api/tasks → Create task
PUT /api/tasks/<id> → Update task
DELETE /api/tasks/<id> → Delete tas

🧪 Testing
You can test APIs using:
Postman
Browser (GET requests)
Frontend UI



Create a .env file:

DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your_secret_key
📌 Important Notes
Passwords are stored in hashed format
Each user sees only their own tasks
Database uses relational integrity (foreign keys)
