import base64
import os
import io
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
    session,
)
from flask_session import Session
from PIL import Image

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])
INPUT_NAME = "input_image.png"
OUTPUT_NAME = "output_image.png"

random_key = os.urandom(12)

app = Flask(__name__)
app.secret_key = random_key
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# Check for allowed filenames
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Converts a file to an OpenCV mat
def file_to_mat(file):
    pil_image = Image.open(file)
    numpy_image = np.array(pil_image)
    mat = cv.cvtColor(numpy_image, cv.COLOR_RGB2BGR)
    return mat


# Converts a PIL Image to an OpenCV mat
def image_to_mat(image):
    numpy_image = np.array(image)
    mat = cv.cvtColor(numpy_image, cv.COLOR_RGB2BGR)
    return mat


# Creates a placeholder image mat given an image
def generate_placeholder(image):
    img_mat = cv.cvtColor(
        np.array(image), cv.COLOR_RGB2BGR
    )  # Convert directly to mat to get dimensions
    ph_img = Image.new("RGB", (img_mat.shape[1], img_mat.shape[0]))
    return ph_img


# Converts an Image object to encoded byte data (png format)
def image_to_encoded_bytes(image):
    byte_data = io.BytesIO()
    image.save(byte_data, "png")
    encoded_bytes = base64.b64encode(byte_data.getvalue())
    return encoded_bytes


# Converts OpenCV mat to PIL Image object
def mat_to_image(mat):
    mat = cv.cvtColor(mat, cv.COLOR_BGR2RGB)  # Colour space adjustment
    image = Image.fromarray(mat)  # Conversion to PIL Image
    return image


# Converts OpenCV mat to PIL Image object, preserves transparency
def mat_to_image_trans(mat):
    mat = cv.cvtColor(mat, cv.COLOR_BGRA2RGBA)  # Colour space adjustment
    image = Image.fromarray(mat)  # Conversion to PIL Image
    return image


# Clears session values
def clear_session():
    session["input_file"] = None
    session["output_img"] = None
    session["selection"] = None
    return None


# Index page
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if request.files:
            if "file" not in request.files:
                flash("No file part")
                return redirect(request.url)
            file = request.files["file"]
            if file.filename == "":
                flash("No selected file")
                return redirect(request.url)
            if file and allowed_file(file.filename):
                # For HTML
                image = Image.open(file)
                output_img = generate_placeholder(image)
                encoded_input = image_to_encoded_bytes(image)  # Input image
                encoded_output = image_to_encoded_bytes(output_img)  # Placeholder image
                session["input_file"] = image  # Session copy of input image
                return render_template(
                    "preview.html",
                    img_data=encoded_input.decode("utf-8"),
                    out_data=encoded_output.decode("utf-8"),
                    imgwidth=image.width,
                    imgheight=image.height,
                )

        if int(request.form["xPos"]) > 0:
            # Receive and convert jQuery values for selection
            x_pos = int(request.form["xPos"])
            y_pos = int(request.form["yPos"])
            w_sel = int(request.form["wSel"])
            h_sel = int(request.form["hSel"])
            session["selection"] = (x_pos, y_pos, w_sel, h_sel)
            return "Got pos values"  # Not actually used as only occurs on POST handle

    elif session.get("input_file") != None and session.get("selection") != None:
        # Open input image, convert to array, run it through algorithm
        selection = session["selection"]
        img_in = session["input_file"]
        mat_in = image_to_mat(img_in)
        session["selection"] = None
        mat_out = GrabCutUI.GrabCutApp.run(GrabCutUI.GrabCutApp, mat_in, selection)
        # Convert output to Image for session, bytes for HTML
        img_out = mat_to_image_trans(mat_out)
        session["output_img"] = img_out
        encoded_output = image_to_encoded_bytes(img_out)
        # Get encoded input bytes for HTML
        encoded_image = image_to_encoded_bytes(img_in)
        return render_template(
            "preview.html",
            img_data=encoded_image.decode("utf-8"),
            out_data=encoded_output.decode("utf-8"),
            imgwidth=img_in.width,
            imgheight=img_in.height,
        )
    else:
        clear_session()
        return render_template("index.html")


@app.route("/download")
def download():
    if session.get("output_img") != None:  # If an output exists in the session
        out_data = io.BytesIO()
        dl_copy = session["output_img"]
        dl_copy.save(out_data, "png")
        out_data.seek(0)
        return send_file(
            out_data,
            mimetype="image/png",
            as_attachment=True,
            attachment_filename="output_image",
        )
    return ("", 204)


if __name__ == "__main__":
    app.run()
