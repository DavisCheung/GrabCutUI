# grabCutUI
 Simple application that uses the Grabcut algorithm in OpenCV to remove the background of an image.

## Introduction
This project was made to showcase a simple implementation of the GrabCut algorithm. It adds a simple UI, file IO, and selection tool to the GrabCut demo found in the OpenCV tutorial.

## Technologies
This project used:
- Python 3.10
- numpy 1.22.3
- opencv-python 4.5.5.64

Note. This app may not work on non-windows operating systems, but this has not been tested.

## How to use
To run this project, ensure that the above packages are installed, clone the repo, and run grabCutUI.py.

- When the program runs, it will immediately open your file explorer to the "./Test_Images" directory and wait until an image file is selected (.png, .jpg, or .jpeg).

[File Explorer Example](./readmepics/fileExplorer.PNG)

- Once a file has been selected, two windows; one labelled "Image Selection" and another "Preview" will pop up.

[Initial UI Example](./readmepics/preSelection.PNG)

- Click and drag in the "Image Selection" window to make a rectangular selection over the thing you wish to cut-out from the image.

[Selection Example](./readmepics/postSelection.PNG)

- Once the green rectangle has been placed, press the ENTER key to run the GrabCut algorithm. After a couple minutes, the now cut-out image will be visible in the "Preview" window.

[Cut Image Example](./readmepics/cutImageExample.PNG)

- You may re-select the rectangular bounds and press ENTER again to re-process the new selection.

- To close the app, press the ESC key - this will also save a copy of the cropped image into the local directory as "cutImage.png" (Functionally, this means that this program could also be used to covnert any image to a .png if you so desire)

[Final Image Example](./readmepics/nice.png)

## Sources
This project was based on the OpenCV tutorial demo for GrabCut, and built on the UI-less demo code as a base.
(https://docs.opencv.org/3.4/d8/d83/tutorial_py_grabcut.html)