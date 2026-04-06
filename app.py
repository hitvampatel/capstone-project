from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'college2024secret'

DB_PATH = 'events.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            venue TEXT NOT NULL,
            category TEXT NOT NULL,
            organizer TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            student_name TEXT NOT NULL,
            student_email TEXT NOT NULL,
            roll_no TEXT NOT NULL,
            registered_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
    ''')
    # Seed some sample events if empty
    count = conn.execute('SELECT COUNT(*) FROM events').fetchone()[0]
    if count == 0:
        sample_events = [
            ('Tech Fest 2024', 'Annual college technology festival with competitions and workshops.', '2024-12-15', '10:00', 'Main Auditorium', 'Technical', 'CSE Department'),
            ('Cultural Night', 'A celebration of art, music and dance by students.', '2024-12-20', '18:00', 'Open Ground', 'Cultural', 'Student Council'),
            ('Hackathon 2024', '24-hour coding hackathon open to all students.', '2024-12-22', '09:00', 'Lab Block A', 'Technical', 'Coding Club'),
        ]
        conn.executemany('INSERT INTO events (title, description, date, time, venue, category, organizer) VALUES (?,?,?,?,?,?,?)', sample_events)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db()
    category = request.args.get('category', '')
    if category:
        events = conn.execute('SELECT * FROM events WHERE category=? ORDER BY date ASC', (category,)).fetchall()
    else:
        events = conn.execute('SELECT * FROM events ORDER BY date ASC').fetchall()
    conn.close()
    return render_template('index.html', events=events, selected_category=category)

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    conn = get_db()
    event = conn.execute('SELECT * FROM events WHERE id=?', (event_id,)).fetchone()
    regs = conn.execute('SELECT * FROM registrations WHERE event_id=? ORDER BY registered_at DESC', (event_id,)).fetchall()
    conn.close()
    if not event:
        flash('Event not found!', 'error')
        return redirect(url_for('index'))
    return render_template('event_detail.html', event=event, registrations=regs)

@app.route('/register/<int:event_id>', methods=['POST'])
def register(event_id):
    name = request.form.get('student_name', '').strip()
    email = request.form.get('student_email', '').strip()
    roll = request.form.get('roll_no', '').strip()
    if not name or not email or not roll:
        flash('All fields are required!', 'error')
        return redirect(url_for('event_detail', event_id=event_id))
    conn = get_db()
    existing = conn.execute('SELECT id FROM registrations WHERE event_id=? AND roll_no=?', (event_id, roll)).fetchone()
    if existing:
        flash('You are already registered for this event!', 'warning')
        conn.close()
        return redirect(url_for('event_detail', event_id=event_id))
    conn.execute('INSERT INTO registrations (event_id, student_name, student_email, roll_no) VALUES (?,?,?,?)',
                 (event_id, name, email, roll))
    conn.commit()
    conn.close()
    flash(f'Successfully registered for the event! Welcome, {name}!', 'success')
    return redirect(url_for('event_detail', event_id=event_id))

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        desc = request.form.get('description', '').strip()
        date = request.form.get('date', '').strip()
        time = request.form.get('time', '').strip()
        venue = request.form.get('venue', '').strip()
        category = request.form.get('category', '').strip()
        organizer = request.form.get('organizer', '').strip()
        if not all([title, date, time, venue, category, organizer]):
            flash('All required fields must be filled!', 'error')
            return render_template('add_event.html')
        conn = get_db()
        conn.execute('INSERT INTO events (title, description, date, time, venue, category, organizer) VALUES (?,?,?,?,?,?,?)',
                     (title, desc, date, time, venue, category, organizer))
        conn.commit()
        conn.close()
        flash('Event added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_event.html')

@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    conn = get_db()
    conn.execute('DELETE FROM registrations WHERE event_id=?', (event_id,))
    conn.execute('DELETE FROM events WHERE id=?', (event_id,))
    conn.commit()
    conn.close()
    flash('Event deleted successfully.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    print("\n✅ Student Event Portal is running!")
    print("🌐 Open your browser and go to: http://127.0.0.1:5000\n")
    app.run(debug=True)
