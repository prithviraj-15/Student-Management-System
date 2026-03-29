from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create Database
def init_db():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            course TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home Page
@app.route('/')
def index():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    conn.close()
    return render_template('index.html', students=students)

# Add Student
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']

        conn = sqlite3.connect('students.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
                    (name, age, course))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add.html')

# Delete Student
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Edit Student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']

        cur.execute("UPDATE students SET name=?, age=?, course=? WHERE id=?",
                    (name, age, course, id))
        conn.commit()
        conn.close()
        return redirect('/')

    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()
    conn.close()
    return render_template('edit.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)