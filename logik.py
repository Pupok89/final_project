import sqlite3

def create_school_db():
    conn = sqlite3.connect('school_db.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                 id INTEGER PRIMARY KEY,
                 name TEXT,
                 grades TEXT,
                 homework TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS teachers (
                 id INTEGER PRIMARY KEY,
                 name TEXT)''')
    conn.commit()
    conn.close()

def create_schedule_db():
    conn = sqlite3.connect('schedule.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS schedule (
                 day TEXT PRIMARY KEY,
                 subjects TEXT)''')
    conn.commit()
    conn.close()

def add_schedule(day, subjects):
    conn = sqlite3.connect('schedule.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO schedule (day, subjects) VALUES (?, ?)', (day, subjects))
    conn.commit()
    conn.close()

def get_schedule(day):
    conn = sqlite3.connect('schedule.db')
    c = conn.cursor()
    c.execute('SELECT subjects FROM schedule WHERE day = ?', (day,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def add_student(name):
    conn = sqlite3.connect('school_db.db')
    c = conn.cursor()
    c.execute('INSERT INTO students (name, grades, homework) VALUES (?, ?, ?)', (name, '', ''))
    conn.commit()
    conn.close()

def get_student(name):
    conn = sqlite3.connect('school_db.db')
    c = conn.cursor()
    c.execute('SELECT grades, homework FROM students WHERE name = ?', (name,))
    result = c.fetchone()
    conn.close()
    return result

def update_student_grades(name, grades, homework):
    conn = sqlite3.connect('school_db.db')
    c = conn.cursor()
    c.execute('UPDATE students SET grades = ?, homework = ? WHERE name = ?', (grades, homework, name))
    conn.commit()
    conn.close()

def add_teacher(name):
    conn = sqlite3.connect('school_db.db')
    c = conn.cursor()
    c.execute('INSERT INTO teachers (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def is_teacher(name):
    conn = sqlite3.connect('school_db.db')
    c = conn.cursor()
    c.execute('SELECT * FROM teachers WHERE name = ?', (name,))
    result = c.fetchone()
    conn.close()
    return result is not None

# Инициализация обеих баз
create_school_db()
create_schedule_db()