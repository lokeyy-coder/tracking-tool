from flask import Flask, request, render_template, send_file
import sqlite3
import pandas as pd
from io import BytesIO

app = Flask(__name__)

# Database setup function
def init_db():
    conn = sqlite3.connect('kopiko_habit_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER,
            month TEXT,
            day INTEGER,
            time TEXT,
            event TEXT,
            size TEXT,
            post_food INTEGER,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect('kopiko_habit_tracker.db')
    cursor = conn.cursor()

    if request.method == "POST":
        if "submit" in request.form:
            year = int(request.form["year"])
            month = request.form["month"]
            day = int(request.form["day"])
            time = request.form["time"]
            event = request.form["event"]
            size = request.form["size"]
            post_food = int(request.form["post_food"])

            cursor.execute('''
                INSERT INTO habits (year, month, day, time, event, size, post_food, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
            ''', (year, month, day, time, event, size, post_food))

            conn.commit()

        elif "delete" in request.form:
            timestamp = request.form["timestamp"]
            cursor.execute("DELETE FROM habits WHERE timestamp = ?", (timestamp,))
            conn.commit()

    cursor.execute("SELECT * FROM habits ORDER BY timestamp DESC LIMIT 10")
    last_entries = cursor.fetchall()

    cursor.execute("SELECT timestamp FROM habits")
    timestamps = cursor.fetchall()
    timestamps = [ts[0] for ts in timestamps]

    summary = f"{len(last_entries)} recent entries."

    conn.close()

    return render_template("index.html", last_entries=last_entries, summary=summary, timestamps=timestamps)

@app.route("/download", methods=["GET"])
def download():
    conn = sqlite3.connect('kopiko_habit_tracker.db')
    df = pd.read_sql_query("SELECT * FROM habits", conn)
    conn.close()

    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    return send_file(output, as_attachment=True, download_name="kopiko_habit_tracker.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
