# Chemical Equipment Visualizer

A full-stack application for uploading and analyzing chemical equipment datasets with automatic summary generation, equipment distribution charts, history tracking, authentication, and PDF report export.

## The project includes:

    🌐 Web UI (React + Tailwind + Chart.js)

    🖥 Desktop UI (PyQt5 + Matplotlib)

    ⚙️ Backend API (Django + DRF)

    🔐 Authentication (HTTP Basic Auth)

    📊 Chart visualization

    📄 PDF report generation

    🕘 Upload history with per-dataset actions

## Project Structure

```bash
chemical-equipment-visualizer/
│
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── db.sqlite3
│   ├── equipment_backend/      # Django project
│   └── equipment/              # Django app (APIs, models, views)
│
├── frontend/                   # React web UI
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── desktop/                    # PyQt5 desktop app
│   └── app.py
│
└── README.md

```

## Features:

Dataset Upload:

- Upload CSV datasets

- Automatic parsing and validation

- Stored with timestamp

Summary Generation

- Total equipment count

- Average flowrate, pressure, temperature

- Equipment type distribution

Visualization

- Bar chart of equipment distribution

- Web: Chart.js

- Desktop: Matplotlib

History

- Stores previous uploads

- View previous summaries instantly

- Download PDF per dataset

Authentication

- Login required (web + desktop)

- Backend protected with Basic Auth

- UI locked until login succeeds

PDF Reports

- Per-dataset downloadable reports

- Available from web and desktop UI

## Requirements: 

- Python 3.10+

- Node.js 18+

- pip

- npm

- virtualenv (recommended)

## Backend Setup (Django API)

1️⃣ Go to backend folder
```
cd backend
```

2️⃣ Create & activate virtual environment
```
python -m venv venv
venv\Scripts\activate
```
3️⃣ Install dependencies
```
pip install -r requirements.txt
```
4️⃣ Run migrations
```
python manage.py migrate
```
5️⃣ Start backend server
```
python manage.py runserver
```

Backend runs at:
```
http://127.0.0.1:8000/
```

## Web Frontend Setup (React)

1️⃣ Go to frontend folder
```
cd frontend
```
2️⃣ Install packages
```
npm install
```
3️⃣ Start dev server
```
npm run dev
```

Web app runs at:
```
http://localhost:5173
```

## Desktop App Setup (PyQt5)

1️⃣ Activate backend virtual environment
Desktop app uses backend dependencies:
```
cd backend
venv\Scripts\activate
```
2️⃣ Run desktop app
```
cd desktop
python app.py
```

## Features:

- Login dialog

- Fullscreen main window

- Upload + history + chart + PDF

- Logout returns to login screen

## Authentication

Both web and desktop apps use HTTP Basic Authentication.

Example test credentials :
```
username: user2
password: qwer
```

## API Endpoints
```
POST   /api/upload/
GET    /api/history/
GET    /api/dataset/<id>/
GET    /api/report/<id>/
```
All endpoints require authentication.

## Requirements.txt
```
asgiref==3.11.0
certifi==2026.1.4
charset-normalizer==3.4.4
contourpy==1.3.3
cycler==0.12.1
Django==6.0.1
django-cors-headers==4.9.0
djangorestframework==3.16.1
fonttools==4.61.1
idna==3.11
kiwisolver==1.4.9
matplotlib==3.10.8
numpy==2.4.1
packaging==26.0
pandas==3.0.0
pillow==12.1.0
pyparsing==3.3.2
PyQt5==5.15.11
PyQt5-Qt5==5.15.2
PyQt5_sip==12.18.0
python-dateutil==2.9.0.post0
reportlab==4.4.9
requests==2.32.5
six==1.17.0
sqlparse==0.5.5
tzdata==2025.3
urllib3==2.6.3
```

## Author

Nilabh Sharma