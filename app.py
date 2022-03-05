import csv
from flask import Flask, render_template, request
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

@app.route("/", methods=["GET", "POST"])
def index():
    # Provide form
    if request.method == "GET":
        return render_template("index.html")

    # Find reviewers
    reviewed = reviews(request.form.get("reviewers"), request.form.get("reviewees"))[0]
    return render_template("reviewers.html", reviewed=reviewed)