import csv
from flask import Flask, render_template, request, redirect, flash
import io
import os
import random
from reviews import reviews
from tempfile import mkdtemp

app = Flask(__name__)

# Following two blocks from C$50 Finance
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 's3cr3t_p@ssw0rd'

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    # Provide form
    if request.method == "GET":
        return render_template("index.html")

    # Get form data
    try:
        (reviewers_file, reviewees_file) = (request.files["reviewers"], request.files["reviewees"])
        reviewers = io.StringIO(reviewers_file.stream.read().decode("UTF8"), newline=None)
        reviewees = io.StringIO(reviewees_file.stream.read().decode("UTF8"), newline=None)
    except:
        flash("Invalid file(s)")
        return redirect("/")

    try:
        num_reviewers = int(request.form.get("num_reviewers"))
    except:
        flash("Invalid number of reviewers")
        return redirect("/")

    # Provide error messages
    output = reviews(reviewers, reviewees, num_reviewers)
    if isinstance(output, str):
        flash(output)
        return redirect("/")

    matchings = output["matchings"]
    reviewers_file.close()
    reviewees_file.close()

    # Create csv data
    csv_data = []

    # Create headers
    row = ["Reviewee"]
    for i in range(1, num_reviewers + 1):
        row.append("Reviewer " + str(i))
    csv_data.append(row)

    for reviewee in matchings:
        row = [reviewee]
        for reviewer in matchings[reviewee]:
            row.append(reviewer)
        csv_data.append(row)

    return render_template("reviewers.html", csv_data=csv_data, matchings=matchings, reviewees=matchings.keys(), num_reviewers=num_reviewers)

