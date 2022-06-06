import csv
from flask import Flask, render_template, request, flash
import io
import os
import random
from reviews import reviews
from tempfile import mkdtemp

app = Flask(__name__)

# Following two blocks from C$50 Finance
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# For csv uploads
app.config['UPLOAD_FOLDER'] = "/uploads"
ALLOWED_EXTENSIONS = {"csv"}
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    # Provide form
    if request.method == "GET":
        return render_template("index.html")

    # Get form data
    (reviewers_file, reviewees_file) = (request.files["reviewers"], request.files["reviewees"])
    reviewers = io.StringIO(reviewers_file.stream.read().decode("UTF8"), newline=None)
    reviewees = io.StringIO(reviewees_file.stream.read().decode("UTF8"), newline=None)

    output = reviews(reviewers, reviewees, 2)
    if isinstance(output, str):
        flash(output)
        return redirect("/")

    matchings = output["matchings"]
    reviewers_file.close()
    reviewees_file.close()
    return render_template("reviewers.html", matchings=matchings, reviewees=matchings.keys())


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


# From https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
