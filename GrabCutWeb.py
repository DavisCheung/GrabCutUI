from genericpath import exists
import os
import shutil
import GrabCutUI
import numpy as np
import cv2 as cv
from flask import (
    Flask,
    flash,
    render_template,
    request,
    redirect,
    send_file,
    url_for,
)
from PIL import Image

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])
UPLOAD_FOLDER = "static/uploads/"
INPUT_NAME = "input_image.png"
OUTPUT_NAME = "output_image.png"

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Check for allowed filenames
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Converts a file to an OpenCV mat
def file_to_img(file):
    pil_image = Image.open(file)
    numpy_image = np.array(pil_image)
    img = cv.cvtColor(numpy_image, cv.COLOR_RGB2BGR)
    return img


# Clears uploads folder
def initialize():
    shutil.rmtree("static/uploads/")
    os.makedirs("static/uploads/")


initialize()  # Clear previous uploads on launch

# Creates a placeholder image mat given an image file
def generate_placeholder(file):
    img_mat = file_to_img(file)  # Convert directly to mat to get dimensions
    ph_img = Image.new("RGB", (img_mat.shape[1], img_mat.shape[0]))
    return ph_img


# Index page
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Check if post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # Submits empty part w/o filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # For HTML
            image = Image.open(file)
            filename = INPUT_NAME
            filename_out = OUTPUT_NAME
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename), "png")
            output_img = generate_placeholder(file)  # Placeholder for output image
            output_img.save(
                os.path.join(app.config["UPLOAD_FOLDER"], filename_out), "png"
            )

            # For OpenCV
            # img_test = file_to_img(file)

            """
            retval, buffer = cv.imencode(
                ".png", GrabCutUI.GrabCutApp().run(img_test)
            )
            response = make_response(buffer.tobytes())
            response.headers["Content-Type"] = "image/png"
            """
            return redirect("/preview")
            # return render_template("preview.html", imagename=filename, outname=filename_out, imgwidth=img_width, imgheight=img_height)

    return render_template("index.html")


@app.route("/preview", methods=["GET", "POST"])
def preview():
    if request.method == "POST":
        # Receive and convert jQuery values for selection
        x_pos = int(request.form["xPos"])
        y_pos = int(request.form["yPos"])
        w_sel = int(request.form["wSel"])
        h_sel = int(request.form["hSel"])
        # Open input image, convert to array, run it through algorithm
        img_in = Image.open(os.path.join(app.config["UPLOAD_FOLDER"], INPUT_NAME))
        img_width = img_in.width
        img_height = img_in.height
        mat_in = cv.cvtColor(np.array(img_in), cv.COLOR_RGB2BGR)
        selection: tuple[int] = (x_pos, y_pos, w_sel, h_sel)
        mat_out = GrabCutUI.GrabCutApp.run(GrabCutUI.GrabCutApp, mat_in, selection)
        # Convert output back to PIL Image
        mat_out = cv.cvtColor(mat_out, cv.COLOR_BGR2RGB)
        img_out = Image.fromarray(mat_out)
        img_out.save(os.path.join(app.config["UPLOAD_FOLDER"], OUTPUT_NAME))
        return redirect(url_for("preview"))

    if exists(os.path.join(app.config["UPLOAD_FOLDER"], INPUT_NAME)):
        img_pv = Image.open(os.path.join(app.config["UPLOAD_FOLDER"], INPUT_NAME))
        img_width = img_pv.width
        img_height = img_pv.height
        return render_template(
            "preview.html",
            imagename=INPUT_NAME,
            outname=OUTPUT_NAME,
            imgwidth=img_width,
            imgheight=img_height,
        )
    else:
        return redirect("/")  # Redirect if user shouldn't be here yet


@app.route("/download")
def download():
    if exists(os.path.join("static/uploads/", OUTPUT_NAME)):
        path = os.path.join("static/uploads/", OUTPUT_NAME)
        return send_file(path, as_attachment=True)
    else:
        return redirect("/")  # Redirect if user shouldn't be here yet
