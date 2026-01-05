from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_NAME = "database.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            gender TEXT,
            course TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    gender = request.form['gender']
    course = request.form['course']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO user_data (name, gender, course) VALUES (?, ?, ?)",
        (name, gender, course)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('view_data'))

@app.route('/view')
def view_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_data")
    rows = cursor.fetchall()

    conn.close()
    return render_template("view.html", data=rows)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM user_data WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('view_data'))

# if __name__ == '__main__':
#     init_db()
#     app.run(debug=True)



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
