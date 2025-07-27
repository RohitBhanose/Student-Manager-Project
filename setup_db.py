import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject TEXT,
    attended INTEGER,
    total_classes INTEGER
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS cgpa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    semester INTEGER,
    gpa REAL
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    title TEXT,
    deadline TEXT,
    submitted INTEGER DEFAULT 0
)
''')

conn.commit()
conn.close()
print("✅ Database setup complete.")
