# Sweet Shop Management System

A full-stack web application to manage a sweet shop, built with **FastAPI** (backend) and **Vue.js** (frontend).  
Users can browse sweets, add them to a cart, and simulate purchases, while the admin can manage sweets.

---

## Features

- View available sweets with images, names, and prices  
- Search and filter sweets by name or category  
- Add sweets to cart and manage cart items  
- Responsive, user-friendly UI  
- Backend API with CORS enabled for smooth frontend-backend integration  

---

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, SQLite (or any preferred database)  
- **Frontend:** Vue.js, Vite, Tailwind CSS, Axios  
- **Authentication:** JWT token-based authentication (optional)  
- **Version Control:** Git & GitHub  
Frontend runs on: http://localhost:5173
---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/sweetshop.git
cd sweetshop
cd app
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
# source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
Backend runs on: http://127.0.0.1:8000

Usage:

Open the frontend URL in your browser.
Browse sweets, search, and add them to the cart.
Admin can manage sweets via backend APIs.

sweetshop/
├─ app/                  # Backend
│  ├─ main.py
│  ├─ models.py
│  ├─ schemas.py
│  ├─ auth.py
│  └─ database.py
├─ frontend-vue/         # Frontend
│  ├─ src/
│  ├─ package.json
│  └─ vite.config.js
├─ requirements.txt      # Backend dependencies
└─ README.md

Contributing

Fork the repository
Create a feature branch (git checkout -b feature-name)
Commit your changes (git commit -m 'feat: description')
Push to branch (git push origin feature-name)
Open a Pull Request

This project is licensed under the MIT License.

