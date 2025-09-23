🍬 Sweet Shop Management System

A full-stack web application to manage a sweet shop, built with FastAPI (backend) and Vue.js (frontend).
Customers can browse sweets, search and purchase items, while admins can add, update, delete, and restock sweets.

✨ Features

👤 User Authentication (JWT-based login & registration)
🛍 Browse & Search sweets by name, category, or price
➕ Purchase sweets (decreases stock, disabled if quantity = 0)
🔧 Admin Management: Add, update, delete, and restock sweets
🎨 Responsive UI with Tailwind CSS
🔒 Role-based access control (User vs. Admin)

🛠 Tech Stack

Backend
FastAPI, SQLAlchemy, SQLite/PostgreSQL
JWT authentication (python-jose, passlib[bcrypt])
Pytest for TDD

Frontend
Vue 3 + Vite
Tailwind CSS
Axios for API requests

DevOps & Workflow
Git & GitHub for version control
TDD (Test-Driven Development) workflow

🚀 Installation & Setup
1. Clone the repository
git clone https://github.com/<your-username>/sweetshop.git
cd sweetshop

2. Backend Setup (FastAPI)
   cd app
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend
uvicorn main:app --reload
Backend runs at: http://127.0.0.1:8000

3. Frontend Setup (Vue + Vite)
cd ../frontend-vue
npm install
npm run dev
Frontend runs at: http://127.0.0.1:5173

📂 Project Structure
sweetshop/
├─ app/                  # Backend (FastAPI)
│  ├─ main.py
│  ├─ models.py
│  ├─ schemas.py
│  ├─ auth.py
│  └─ database.py
├─ frontend-vue/         # Frontend (Vue 3 + Vite)
│  ├─ src/
│  ├─ package.json
│  └─ vite.config.js
├─ requirements.txt      # Python dependencies
└─ README.md             # Project docs

✅ Testing
pytest --cov=app
Generates coverage report and validates all TDD test cases.

🤖 My AI Usage

I used AI tools to speed up development responsibly:
ChatGPT: brainstorming API structure, drafting unit tests, scaffolding Vue components, and writing README sections.
GitHub Copilot: generating repetitive code (form handling, API calls).
Reflection: AI helped accelerate boilerplate and testing, while I manually reviewed, refactored, and implemented business logic to ensure correctness and security.

🤝 Contributing

Fork the repo
Create a feature branch (git checkout -b feature-name)
Commit changes (git commit -m 'feat: description')
Push to branch (git push origin feature-name)
Open a Pull Request

📜 License
This project is licensed under the MIT License.
