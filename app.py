import csv
from flask import Flask, render_template, request, redirect
from datetime import datetime
from key import *

app = Flask(__name__)
CSV_FILE = "data.csv"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle form submission for adding a new task
        task = request.form["task"]
        project = request.form["project"]
        deadline = request.form["deadline"]
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Determine the next ID
        with open(CSV_FILE, "r", newline="") as file:
            reader = csv.reader(file)
            rows = list(reader)
            new_id = len(rows)  # Use the row count as the ID

        # Add new entry to CSV with completed defaulting to 0 (incomplete)
        with open(CSV_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([new_id, task, project, date_added, deadline, 0])

        return redirect("/")

    # Fetch all entries from CSV
    with open(CSV_FILE, "r", newline="") as file:
        reader = csv.reader(file)
        entries = list(reader)[1:]  # Skip the header row

    # Filter only incomplete tasks (completed = 0)
    incomplete_entries = [entry for entry in entries if entry[5] == "0"]

    # Sort entries by deadline (ascending)
    entries_sorted = sorted(incomplete_entries, key=lambda x: datetime.strptime(x[4], "%Y-%m-%d"))

    return render_template("index.html", entries=entries_sorted)

@app.route("/complete/<task_id>", methods=["POST"])
def complete_task(task_id):
    # Mark a task as completed by updating the CSV
    with open(CSV_FILE, "r", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Update the row where the ID matches the task_id
    for row in rows:
        if row[0] == task_id:
            row[5] = "1"  # Set completed to 1 (True)

    # Write the updated data back to the CSV
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=portto, debug=True)
