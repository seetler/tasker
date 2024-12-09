import csv
from flask import Flask, render_template, request, redirect
from datetime import datetime
from key import *  # Ensure this file contains the 'portto' variable

app = Flask(__name__)
CSV_FILE = "data.csv"

# Function to read CSV entries
def read_csv():
    with open(CSV_FILE, "r", newline="") as file:
        reader = csv.reader(file)
        return list(reader)

# Function to write CSV entries
def write_csv(rows):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

# Route to display tasks and handle adding/updating tasks
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_id = request.form.get("id")
        task = request.form["task"]
        project = request.form["project"]
        deadline = request.form["deadline"]
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        rows = read_csv()

        if task_id:  # If ID exists, it's an edit operation
            for row in rows:
                if row[0] == task_id:
                    row[1] = task
                    row[2] = project
                    row[4] = deadline
                    break
        else:  # Otherwise, it's a new task
            new_id = len(rows)
            rows.append([str(new_id), task, project, date_added, deadline, '0'])

        write_csv(rows)
        return redirect("/")

    # Fetch all entries from CSV where completed is 0
    rows = read_csv()
    entries = [row for row in rows[1:] if row[5] == '0']

    return render_template("index.html", entries=entries, show_edit_form=False)

# Route to mark a task as completed
@app.route("/complete/<id>", methods=["POST"])
def complete(id):
    rows = read_csv()
    for row in rows:
        if row[0] == id:
            row[5] = '1'  # Mark task as completed
            break
    write_csv(rows)
    return redirect("/")

# Route to handle editing a specific task by ID
@app.route("/edit/<id>")
def edit(id):
    rows = read_csv()
    entry = next((row for row in rows if row[0] == id), None)
    return render_template("index.html", entries=rows[1:], edit_entry=entry, show_edit_form=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=portto, debug=True)
