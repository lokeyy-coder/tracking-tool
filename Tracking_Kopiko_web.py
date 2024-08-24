from flask import Flask, render_template, request
from openpyxl import load_workbook

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        year = request.form['year']
        month = request.form['month']
        day = request.form['day']
        time = request.form['time']
        event = request.form['event']
        size = request.form['size']
        post_food = request.form['post_food']

        # Load the existing Excel workbook
        workbook = load_workbook("Kopiko_Habit_Tracker.xlsx")
        sheet = workbook.active

        # Find the next available row in the sheet
        next_row = sheet.max_row + 1

        # Write the data to the next row
        sheet.cell(row=next_row, column=1, value=year)
        sheet.cell(row=next_row, column=2, value=month)
        sheet.cell(row=next_row, column=3, value=day)
        sheet.cell(row=next_row, column=4, value=time)
        sheet.cell(row=next_row, column=5, value=event)
        sheet.cell(row=next_row, column=6, value=size)
        sheet.cell(row=next_row, column=7, value=post_food)

        # Save the workbook
        workbook.save("Kopiko_Habit_Tracker.xlsx")

        # Load the workbook again to read the last 10 entries
        workbook = load_workbook("Kopiko_Habit_Tracker.xlsx")
        sheet = workbook.active

        # Get the last 10 entries
        num_rows = sheet.max_row
        last_10_entries = []
        for row in range(max(num_rows - 9, 1), num_rows + 1):
            entry = [sheet.cell(row=row, column=col).value for col in range(1, 8)]
            last_10_entries.append(entry)

        # Pass the success message and last 10 entries to the template
        summary = f"Successfully submitted: Event: {event} at {time}, {day}/{month}/{year}, Size: {size}, After Food: {post_food}"
        return render_template('index.html', summary=summary, last_entries=last_10_entries)

    return render_template('index.html', summary='', last_entries=[])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
