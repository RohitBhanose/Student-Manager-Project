# ==========================================
# Complete Flask App: Student Manager (UI Enhanced)
# ==========================================

from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
ADMIN_EMAIL = 'admin@example.com'

# -----------------------
# Database Connection
# -----------------------
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------
# Routes
# -----------------------
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM students WHERE email = ?', (email,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO students (name, email, password) VALUES (?, ?, ?)',
                         (name, email, password))
            conn.commit()
        except:
            return render_template('signup.html', error='Email already exists')
        conn.close()
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user_id = session['user_id']
    conn = get_db_connection()
    attendance = conn.execute('SELECT * FROM attendance WHERE student_id = ?', (user_id,)).fetchall()
    cgpa = conn.execute('SELECT * FROM cgpa WHERE student_id = ?', (user_id,)).fetchall()
    assignments = conn.execute('SELECT * FROM assignments WHERE student_id = ?', (user_id,)).fetchall()
    conn.close()
    return render_template('dashboard.html', attendance=attendance, cgpa=cgpa, assignments=assignments)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/add_attendance', methods=['GET', 'POST'])
def add_attendance():
    if 'user_id' not in session:
        return redirect('/')
    if request.method == 'POST':
        subject = request.form['subject']
        attended = int(request.form['attended'])
        total = int(request.form['total'])
        conn = get_db_connection()
        conn.execute('INSERT INTO attendance (student_id, subject, attended, total_classes) VALUES (?, ?, ?, ?)',
                     (session['user_id'], subject, attended, total))
        conn.commit()
        conn.close()
        return redirect('/dashboard')
    return render_template('add_attendance.html')

@app.route('/add_cgpa', methods=['GET', 'POST'])
def add_cgpa():
    if 'user_id' not in session:
        return redirect('/')
    if request.method == 'POST':
        semester = int(request.form['semester'])
        gpa = float(request.form['gpa'])
        conn = get_db_connection()
        conn.execute('INSERT INTO cgpa (student_id, semester, gpa) VALUES (?, ?, ?)',
                     (session['user_id'], semester, gpa))
        conn.commit()
        conn.close()
        return redirect('/dashboard')
    return render_template('add_cgpa.html')

@app.route('/add_assignment', methods=['GET', 'POST'])
def add_assignment():
    if 'user_id' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        deadline = request.form['deadline']
        submitted = 1 if request.form.get('submitted') == 'yes' else 0  # Convert checkbox to 1 or 0

        conn = get_db_connection()
        conn.execute('INSERT INTO assignments (student_id, title, deadline, submitted) VALUES (?, ?, ?, ?)',
                     (session['user_id'], title, deadline, submitted))
        conn.commit()
        conn.close()
        return redirect('/dashboard')
    return render_template('add_assignment.html')

@app.route('/delete_assignment/<int:assignment_id>', methods=['POST'])
def delete_assignment(assignment_id):
    if 'user_id' not in session:
        return redirect('/')
    conn = get_db_connection()
    conn.execute('DELETE FROM assignments WHERE id = ? AND student_id = ?', (assignment_id, session['user_id']))
    conn.commit()
    conn.close()
    return redirect('/dashboard')


@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect('/')
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM students WHERE id = ?', (session['user_id'],)).fetchone()
    if user['email'] != ADMIN_EMAIL:
        return 'Access Denied'
    students = conn.execute('SELECT id, name, email FROM students').fetchall()
    conn.close()
    return render_template('admin.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)
