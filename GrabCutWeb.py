import base64
import fileinput
from genericpath import exists
import io
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

# Creates a placeholder image mat given an image
def generate_placeholder(image):
    img_mat = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)  # Convert directly to mat to get dimensions
    ph_img = Image.new("RGB", (img_mat.shape[1], img_mat.shape[0]))
    return ph_img

def display_new_page(page, input_data, output_date, width, height):
    return None

global file_processed   # Really dangerous way of doing it, but for the sake of keeping
file_processed = False  # everything on one page, it's the only way I see it working

# Index page
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        print("Post seen")
        '''
        # Check if post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # Submits empty part w/o filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        '''
        if request.files:
            file = request.files["file"]
            if file and allowed_file(file.filename):
                # For HTML
                image = Image.open(file)
                output_img = generate_placeholder(image)
                img_data = io.BytesIO()
                ph_data = io.BytesIO()
                image.save(img_data, "png")
                output_img.save(ph_data, "png")

                global image_file
                image_file = image

                img_width = image.width
                img_height = image.height

                encoded_image = base64.b64encode(img_data.getvalue())
                encoded_output = base64.b64encode(ph_data.getvalue())
                return render_template("preview.html", img_data=encoded_image.decode("utf-8"), out_data=encoded_output.decode("utf-8"), imgwidth=img_width, imgheight=img_height)
        
        if int(request.form["xPos"]) > 0:
            # Receive and convert jQuery values for selection
            global selection
            x_pos = int(request.form["xPos"])
            y_pos = int(request.form["yPos"])
            w_sel = int(request.form["wSel"])
            h_sel = int(request.form["hSel"])
            selection = (x_pos, y_pos, w_sel, h_sel)
            '''
            global file_processed
            file_processed = True
            '''
            # Open input image, convert to array, run it through algorithm
            img_in = image_file
            mat_in = cv.cvtColor(np.array(img_in), cv.COLOR_RGB2BGR)
            mat_out = GrabCutUI.GrabCutApp.run(GrabCutUI.GrabCutApp, mat_in, selection)
            # Convert output back to PIL Image
            mat_out = cv.cvtColor(mat_out, cv.COLOR_BGR2RGB)
            img_out = Image.fromarray(mat_out)
            out_data = io.BytesIO()
            img_out.save(out_data, "png")
            encoded_output = base64.b64encode(out_data.getvalue())

            # Get encoded input
            in_data = io.BytesIO()
            img_in.save(in_data, "png")
            encoded_image = base64.b64encode(in_data.getvalue())
            img_width = img_in.width
            img_height = img_in.height

            # For download
            global dl_copy
            dl_copy = img_out

            file_processed = False
            return render_template("preview.html", img_data=encoded_image.decode("utf-8"), out_data=encoded_output.decode("utf-8"), imgwidth=img_width, imgheight=img_height)
            # return render_template("preview.html")
        '''
    elif file_processed:
        # Open input image, convert to array, run it through algorithm
        img_in = image_file
        mat_in = cv.cvtColor(np.array(img_in), cv.COLOR_RGB2BGR)
        mat_out = GrabCutUI.GrabCutApp.run(GrabCutUI.GrabCutApp, mat_in, selection)
        # Convert output back to PIL Image
        mat_out = cv.cvtColor(mat_out, cv.COLOR_BGR2RGB)
        img_out = Image.fromarray(mat_out)
        out_data = io.BytesIO()
        img_out.save(out_data, "png")
        encoded_output = base64.b64encode(out_data.getvalue())

        # Get encoded input
        in_data = io.BytesIO()
        img_in.save(in_data, "png")
        encoded_image = base64.b64encode(in_data.getvalue())
        img_width = img_in.width
        img_height = img_in.height

        # For download
        global dl_copy
        dl_copy = img_out

        file_processed = False
        return render_template("preview.html", img_data=encoded_image.decode("utf-8"), out_data=encoded_output.decode("utf-8"), imgwidth=img_width, imgheight=img_height)
        '''
    else:
        print("no file")
        return render_template("index.html")

@app.route("/download")
def download():
    out_data = io.BytesIO()
    global dl_copy
    dl_copy.save(out_data, "png")
    out_data.seek(0)
    return send_file(out_data, mimetype="image/png", as_attachment=True, attachment_filename="output_image")

if __name__ == "__main__":
    app.run()