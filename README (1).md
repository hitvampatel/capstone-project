# 🎓 Student Event Portal

A simple local web app for managing college events — built with Python (Flask) + SQLite.

---

## 📁 Project Structure

```
student_events/
├── app.py               ← Python backend (Flask)
├── requirements.txt     ← Dependencies (only Flask)
├── events.db            ← SQLite database (auto-created on first run)
└── templates/
    ├── base.html        ← Common layout
    ├── index.html       ← Event listing page
    ├── event_detail.html← Event detail + registration
    └── add_event.html   ← Add new event form
```

---

## ⚙️ Setup & Run (3 steps)

### Step 1 – Install Flask
Open terminal/command prompt and run:
```
pip install flask
```

### Step 2 – Run the app
Navigate to the project folder and run:
```
python app.py
```

### Step 3 – Open in browser
```
http://127.0.0.1:5000
```

---

## ✅ Features

- View all upcoming events (with category filter)
- Add new events (title, date, time, venue, category, organizer)
- View event details and list of registered students
- Register for an event (name, email, roll number)
- Delete events
- SQLite database stored locally as `events.db`
- 3 sample events auto-loaded on first run

---

## 📦 Requirements

- Python 3.7+
- Flask (`pip install flask`)
- No internet needed — runs 100% locally!
