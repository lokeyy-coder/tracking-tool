@app.route('/', methods=['GET', 'POST'])
def index():
    initialize_excel_file("Kopiko_Habit_Tracker.xlsx")

    if request.method == 'POST':
        if 'delete' in request.form:
            # Handle delete request
            timestamp_to_delete = request.form['timestamp']
            workbook = load_workbook("Kopiko_Habit_Tracker.xlsx")
            sheet = workbook.active

            # Find and delete the row with the matching timestamp
            for row in sheet.iter_rows(min_row=2, max_col=8):
                if row[7].value == timestamp_to_delete:
                    sheet.delete_rows(row[0].row)
                    break

            workbook.save("Kopiko_Habit_Tracker.xlsx")

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
            sheet.cell(row=next_row, column=8, value=timestamp)

            # Save the workbook
            workbook.save("Kopiko_Habit_Tracker.xlsx")

        # Load the workbook again to read the last 10 entries and timestamps
        workbook = load_workbook("Kopiko_Habit_Tracker.xlsx")
        sheet = workbook.active

        # Get the last 10 entries
        num_rows = sheet.max_row
        last_10_entries = []
        for row in range(max(num_rows - 9, 1), num_rows + 1):
            entry = [sheet.cell(row=row, column=col).value for col in range(1, 9)]
            last_10_entries.append(entry)

        # Get all timestamps for deletion
        timestamps = [sheet.cell(row=row, column=8).value for row in range(2, num_rows + 1)]

        summary = "Successfully processed the request."
        return render_template('index.html', summary=summary, last_entries=last_10_entries, timestamps=timestamps)

    # Load the workbook to populate timestamps for the initial GET request
    workbook = load_workbook("Kopiko_Habit_Tracker.xlsx")
    sheet = workbook.active
    timestamps = [sheet.cell(row=row, column=8).value for row in range(2, sheet.max_row + 1)]

    return render_template('index.html', summary='', last_entries=[], timestamps=timestamps)
