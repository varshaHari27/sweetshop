# 🍬 Sweet Shop Management System

A **full-stack web application** to manage a sweet shop, built with **FastAPI** (backend) and **Vue.js** (frontend).  
Customers can browse sweets, search and purchase items, while admins can add, update, delete, and restock sweets.

---

## ✨ Features
- 👤 **User Authentication** (JWT-based login & registration)  
- 🛍 **Browse & Search** sweets by name, category, or price  
- ➕ **Purchase sweets** (stock decreases; disabled if quantity = 0)  
- 🔧 **Admin Panel**: Add, update, delete, and restock sweets  
- 🎨 **Responsive UI** with Tailwind CSS  
- 🔒 **Role-based Access Control** (User vs. Admin)  

---

## 🛠 Tech Stack
**Backend:** FastAPI, SQLAlchemy, SQLite/PostgreSQL, JWT (python-jose, passlib[bcrypt]), Pytest (TDD)  
**Frontend:** Vue 3 + Vite, Tailwind CSS, Axios  
**Workflow:** Git & GitHub, TDD  

---

## 🚀 Installation & Setup

```bash
# 1. Clone Repository
git clone https://github.com/<your-username>/sweetshop.git
cd sweetshop

# 2. Backend Setup (FastAPI)
cd app
python -m venv venv
# Activate virtual environment
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
# Install dependencies
pip install -r requirements.txt
# Run the backend
uvicorn main:app --reload
# Backend available at: http://127.0.0.1:8000

# 3. Frontend Setup (Vue + Vite)
cd ../frontend-vue
npm install
npm run dev
# Frontend available at: http://127.0.0.1:5173

# 4. Project Structure
sweetshop/
├─ app/              # Backend (FastAPI)
│  ├─ main.py
│  ├─ models.py
│  ├─ schemas.py
│  ├─ auth.py
│  └─ database.py
├─ frontend-vue/     # Frontend (Vue 3 + Vite)
│  ├─ src/
│  ├─ package.json
│  └─ vite.config.js
├─ requirements.txt  # Python dependencies
└─ README.md         # Project docs

# 5. Testing
pytest --cov=app
# Generates coverage report and validates all TDD test cases

---

### 🤖 AI Usage

I used AI tools responsibly to accelerate development:
-**ChatGPT:** brainstorming API structure, drafting unit tests, scaffolding Vue components, and refining README docs.
-**GitHub Copilot:** generating repetitive code (form handling, API calls).
-**Manual Review:** All business logic, authentication, and database queries were implemented and verified manually to ensure correctness, maintainability, and security.

---

🤝 Contributing

Fork the repo

Create a feature branch (git checkout -b feat/your-feature)

Commit with Conventional Commits

Push & open a PR

---

📜 License

This project is licensed under the MIT License.
