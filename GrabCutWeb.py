from flask import Flask, render_template, request
from werkzeug import secure_filename
from markupsafe import escape
from GrabCutUI import *

app = Flask(__name__)

@app.route("/upload")
def upload_file():
    return render_template("upload.html")

@app.route("/uploader", methods = ["GET", "POST"])
def upload_file():
    if request.method == "POST":
        f = request.files["file"]
        f.save(secure_filename(f.filename))
        return "file uploaded successfully"

@app.route("/")
def index():
    TITLE = "GrabCutUI App"
    return render_template("index.html", TITLE = TITLE)