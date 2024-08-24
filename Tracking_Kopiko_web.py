from flask import Flask, render_template, request, send_file
from openpyxl import load_workbook, Workbook
import pandas as pd
import os
import io

app = Flask(__name__)

# Initialize the Excel file if it doesn't exist
def initialize_excel_file(filename):
    if not os.path.exists(filename):
        workbook = Workbook()
        sheet = workbook.active
        # Add headers if needed
        sheet.append(["Year", "Month", "Day", "Time", "Event", "Size", "Post Food", "Timestamp"])
        workbook.save(filename)

# Load data into a DataFrame
def load_data(filename):
    return pd.read_excel(filename)

# Save DataFrame back to Excel
def save_data(df, filename):
    with pd.ExcelWriter(filename, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, index=False, header=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    filename = "Kopiko_Habit_Tracker.xlsx"
    initialize_excel_file(filename)
    
    # Load data into DataFrame
    df = load_data(filename)

    summary = ""
    last_entries = []
    timestamps = []

    if request.method == 'POST':
        if 'delete' in request.form:
            # Handle delete request
            timestamp_to_delete = request.form['timestamp']
            df = df[df['Timestamp'] != timestamp_to_delete]
            save_data(df, filename)
            summary = "Entry deleted successfully."

        elif 'submit' in request.form:
            # Handle submit request
            year = request.form['year']
            month = request.form['month']
            day = request.form['day']
            time = request.form['time']
            event = request.form['event']
            size = request.form['size']
            post_food = request.form['post_food']
            timestamp = f"{year}-{month[:3]}-{day} {time}"
            
            # Create a new entry as a DataFrame
            new_entry = pd.DataFrame({
                "Year": [year],
                "Month": [month],
                "Day": [day],
                "Time": [time],
                "Event": [event],
                "Size": [size],
                "Post Food": [post_food],
                "Timestamp": [timestamp]
            })
            
            # Append the new entry to the existing DataFrame
            df = pd.concat([df, new_entry], ignore_index=True)
            save_data(df, filename)
            summary = "Entry added successfully."

        # Get the last 10 entries
        last_entries = df.tail(10).values.tolist()

        # Get all timestamps for deletion
        timestamps = df['Timestamp'].tolist()

    else:
        # Handle initial GET request
        timestamps = df['Timestamp'].tolist()

    return render_template('index.html', summary=summary, last_entries=last_entries, timestamps=timestamps)

@app.route('/export', methods=['POST'])
def export():
    filename = "Kopiko_Habit_Tracker.xlsx"
    df = pd.read_excel(filename)

    # Create an in-memory output file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    output.seek(0)  # Move to the start of the BytesIO object

    # Send the file as a response
    return send_file(output, as_attachment=True, download_name="Kopiko_Habit_Tracker.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
