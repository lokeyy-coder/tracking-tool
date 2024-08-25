from flask import Flask, render_template, request, send_file
import sqlite3
import os
import pandas as pd

app = Flask(__name__)

# Define your database file path
db_file = 'kopiko_habit_tracker.db'

# Check if the database already exists
db_exists = os.path.exists(db_file)

# Establish connection to the SQLite database
conn = sqlite3.connect(db_file)
c = conn.cursor()

# If the database doesn't exist, create the necessary table
if not db_exists:
    c.execute('''CREATE TABLE habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year INTEGER,
                    month TEXT,
                    day INTEGER,
                    time TEXT,
                    event TEXT,
                    size TEXT,
                    post_food INTEGER
                )''')
    conn.commit()

# Close the connection when done
conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    if request.method == "POST":
        if "submit" in request.form:
            # Insert new record into the SQLite database
            new_entry = (request.form["year"], request.form["month"], request.form["day"],
                         request.form["time"], request.form["event"], request.form["size"],
                         request.form["post_food"])
            c.execute('''INSERT INTO habits (year, month, day, time, event, size, post_food)
                         VALUES (?, ?, ?, ?, ?, ?, ?)''', new_entry)
            conn.commit()
        
        elif "delete" in request.form:
            # Delete selected record from the SQLite database
            timestamp = request.form["timestamp"]
            c.execute('DELETE FROM habits WHERE id = ?', (timestamp,))
            conn.commit()
        
        elif "export" in request.form:
            # Export the database contents to an Excel file
            df = pd.read_sql_query("SELECT * FROM habits", conn)
            export_file = "kopiko_habit_tracker_export.xlsx"
            df.to_excel(export_file, index=False)
            return send_file(export_file, as_attachment=True)

    # Retrieve last 10 entries for display
    c.execute('SELECT * FROM habits ORDER BY id DESC LIMIT 10')
    last_entries = c.fetchall()

    # Retrieve all timestamps for the delete dropdown
    c.execute('SELECT id FROM habits ORDER BY id')
    timestamps = [row[0] for row in c.fetchall()]

    conn.close()

    return render_template("index.html", last_entries=last_entries, timestamps=timestamps)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
