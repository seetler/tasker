import csv
from flask import Flask, render_template, request, redirect
from datetime import datetime
from key import *

app = Flask(__name__)
CSV_FILE = "data.csv"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle form submission
        task = request.form["task"]
        project = request.form["project"]
        deadline = request.form["deadline"]
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Determine the next ID
        with open(CSV_FILE, "r", newline="") as file:
            reader = csv.reader(file)
            rows = list(reader)
            new_id = len(rows)  # Use the row count as the ID

        # Add new entry to CSV
        with open(CSV_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([new_id, task, project, date_added, deadline])

        return redirect("/")

    # Fetch all entries from CSV
    with open(CSV_FILE, "r", newline="") as file:
        reader = csv.reader(file)
        entries = list(reader)[1:]  # Skip the header row

    # Sort entries by deadline (ascending)
    entries_sorted = sorted(entries, key=lambda x: datetime.strptime(x[4], "%Y-%m-%d"))

    return render_template("index.html", entries=entries_sorted)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=portto, debug=True)
