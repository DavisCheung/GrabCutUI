from multiprocessing import Process
import os
import tkinter
import numpy as np
import cv2 as cv
from tkinter import filedialog
from tkinter import *
from flask import Flask, flash, request, make_response, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import tempfile

# TO SELF - ADJUST TO SAVE TEMPORARILY LATER
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set (["png", "jpg", "jpeg"])

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

class GrabCutApp:
    GREEN: list[int] = [0, 255, 0]

    # Initialization
    selection: tuple[int] = (0, 0, 1, 1)  # Rectangle for selectiong
    selecting: bool = False  # Flag for selection

    # User-drawn rectangle for selection
    def select_object(self, event, x, y, flags, param):

        if event == cv.EVENT_LBUTTONDOWN:
            self.selecting = True
            self.x_pos = x
            self.y_pos = y

        elif event == cv.EVENT_MOUSEMOVE:
            if self.selecting == True:
                self.img_in = self.ref_img.copy()
                cv.rectangle(self.img_in, (self.x_pos, self.y_pos), (x, y), self.GREEN, 1)
                self.selection = (
                    min(self.x_pos, x),
                    min(self.y_pos, y),
                    abs(self.x_pos - x),
                    abs(self.y_pos - y),
                )

        elif event == cv.EVENT_LBUTTONUP:
            self.selecting = False
            cv.rectangle(self.img_in, (self.x_pos, self.y_pos), (x, y), self.GREEN, 1)
            self.selection = (
                min(self.x_pos, x),
                min(self.y_pos, y),
                abs(self.x_pos - x),
                abs(self.y_pos - y),
            )

    def run(self):
        print("Greetings! Please select an image.")
        print("Note that large images may be hard to edit with this app.\n")

        # File selection
        self.root = tkinter.Tk()
        self.img_name = filedialog.askopenfilename(
            parent=self.root,
            initialdir="./Test_Images",
            title="Please select an image",
            filetypes=[("Images", ["*.png", "*.jpg", "*.jpeg"]), ("all files", "*.*")],
        )

        # Sets image to the selected file; initializes a blank mask
        self.img_in = cv.imread(self.img_name)  # Copy of image for selection use
        self.mask = np.zeros(self.img_in.shape[:2], np.uint8)
        self.img_out = np.zeros(self.img_in.shape, np.uint8)

        self.ref_img = self.img_in.copy()  # Copy of image for algorithm use

        # Windows for Image Selection & Preview
        cv.namedWindow("Image Selection")
        cv.namedWindow("Preview")
        cv.setMouseCallback("Image Selection", self.select_object)

        print("Please draw a rectangle around the object you wish to cut-out.")
        print("After you are finished with your selection, please press ENTER.")
        print("To exit, press ESCAPE.\n")

        # Program loop
        while 1:
            cv.imshow("Image Selection", self.img_in)
            cv.imshow("Preview", self.img_out)
            input = cv.waitKey(1)  # Since the keycode used is assumed to
                                   # be Windows, this may only work on Windows

            if input == 13:  # ENTER key on Windows
                try:
                    # Internally-used arrays in algorithm
                    bg_model = np.zeros((1, 65), np.float64)
                    fg_model = np.zeros((1, 65), np.float64)

                    iter = 5  # Number of algorithm iterations desired

                    cv.grabCut(
                        self.ref_img,
                        self.mask,
                        self.selection,
                        bg_model,
                        fg_model,
                        iter,
                        cv.GC_INIT_WITH_RECT,
                    )

                except:
                    import traceback

                    traceback.print_exc()

            # Makes a new mask from the grabCut mask; output image by multiplication
            mask2 = np.where((self.mask == 2) | (self.mask == 0), 0, 1).astype("uint8")
            self.img_out = self.ref_img * mask2[:, :, np.newaxis]

            if input == 27:  # ESC on Windows
                break

        # Outputs cut image to local directory as "cutImage.png"
        cv.imwrite("./cutImage.png", self.img_out)

# Check for allowed filenames
def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def background_remove(path):
    task = Process(target=rm(path))
    task.start()

def rm(path):
    os.remove(path)

@app.route("/", methods =["GET", "POST"])
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
            filename = secure_filename(file.filename)
            temp_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(temp_path)
            img_test = cv.imread(temp_path)
            retval, buffer = cv.imencode(".png", img_test)
            response = make_response(buffer.tobytes())
            response.headers["Content-Type"] = "image/png"
            background_remove(temp_path)  # Deletes file after processing
            return response
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
            <p><input type=file name=file>
               <input type=submit value=Upload>
        </form>
    '''




'''
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"],
                               filename)

@app.route("/", methods =["GET", "POST"])
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
            filename = secure_filename(file.filename)
            #img_test = cv.imread(file)
            #retval, buffer = cv.imencode(".png", img_test)
            #response = make_response(buffer.tobytes())
            #response.headers["Content-Type"] = "image/png"
            #return response
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("uploaded_file", filename=filename))
    return #Add tiple quotes to make usable again
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
        <p><input type=file name=file>
           <input type=submit value=Upload>
    </form>
    
'''

#GrabCutApp().run()
#cv.destroyAllWindows()
