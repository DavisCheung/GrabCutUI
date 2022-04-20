# GrabCutUI
 A simple application that uses the Grabcut algorithm in OpenCV to remove the background of an image.
 It can be found online here: http://www.grabcutweb.xyz/

## Introduction
 This project was made to showcase a simple implementation of the OpenCV GrabCut algorithm using Flask.
 Code largely revolves around the web integration with Python Flask, Jinja, HTML, and Javascript (jQuery).
 Interesting concepts explored include image manipulation, sessioning, querying, and user interaction.
 
## How to use
 To run this project simply go to: http://www.grabcutweb.xyz/
 
## A Summary of Things Learned
 TL;DR:
 - Image manipulation is much more complicated than you'd expect
 - Web frameworks like Flask and Jinja are wonderful. They make communicating between front/back-end much easier
   - Actually using web frameworks is deceivingly difficult, as documentation is littered with jargon
 - Sessioning is essential to preserving user input between requests
 - Querying is surprisingly simple and straight-forward
 - A little amount of effort is put into making things function, but most is put into making sure things don't break
 
## Technologies
 The following languages/scripts were needed to make this project:
- JavaScript
- Python
- HTML

 The following API's were used:
- jQuery
- OpenCV
- Flask
- Jinja2
- PIL
- flask-session

## The Project, but with Feeling
 Here, I'll explain the project in-depth by file
### GrabCutUI.py
 This is the original project, what used to be a simple python script that built an OpenCV UI out of the demo for GrabCut on the OpenCV wiki (source at bottom). Basically, it:
 - Takes in an image and selection frame
 - Generates a masking layer (like what you use in Photoshop)
 - Generates two matrices
 - Throws everything into a method call, which runs the actual algorithm and returns a processed mask
 - Multiplies the image with the mask to generate an output image
 - Splices out the background through colour channel manipulation

 It's relatively simple code-wise, but the algorithm is much more interesting conceptually.
 
 It basically takes the image and selection frame, and makes a graph (represented by an array) of its pixels with edges corresponding to adjacent pixels.
 It then makes a number of iterative cuts to the graph, seperating sections of the image into essentially "background" and "foreground" regions, a process which is repeated some user-determined number of times to produce a mask of approximately where the algorithm "thinks" the background of the image is.
 This mask can then be multiplied via scalar multiplication with the original image to produce the new, "cut-out" image.
 
 Of course, a lot of the high-level concepts (and subsequently much of the actual meat of the algorithm) is hidden in the paper behind complex equations, but the general idea is pretty simple.
 
 The only other interesting thing it does is convert the image to a 4-channel .png, with the 4th channel being alpha for transparency (the 3 channels are what people mean when they refer to the RGB colour space, for instance)
 
 ### GrabCutWeb.py
  This file contains all of the Flask API calls, and for all intents and purposes is essentially the App itself. It's responsible for taking in user uploads, storing them in memory, and converting them to an array format usable by OpenCV. It also routes page requests, handles jQuery requests, and sends Jinja variables to the two HTML pages for front-end use.
  
  Querying and sessioning enable the project to send information between the front and back-end and store user information between requests, respectively. They're pretty interesting bits of web technology that is taken for granted today.
  
 ### The HTML files
  Pretty simple. Nothing special, except a couple forms and Jinja variables, which allow for back-end values to be communicated to the front-end.
  
 ### Selection.js
  This file is responsible for enabling user creation of a selection frame, as well as the sending of jQuery data to the front-end by JSON. Much of the code was based on a tutorial file (source at bottom) with a number of modifications to ensure that it functioned with the rest of the code. The selection function in the original GrabCutUI.py was used as a reference to ensure that it didn't break anything.
 

## Dependencies
 This project uses:
- Python 3.10
- numpy 1.22.3
- opencv-python-headless 4.5.5.64
- Flask
- Pillow
- MarkupSafe
- gunicorn
- Werkzeug
- Jinja2
- colorama
- itsdangerous
- click
- setuptools
- flask-session

 The project was deployed with Flask using Heroku

## Sources
This project was based on the OpenCV tutorial demo for GrabCut.
(https://docs.opencv.org/3.4/d8/d83/tutorial_py_grabcut.html)
JavaScript selection code was based off a cropping tool from script-tutorials.
(https://www.script-tutorials.com/demos/197/index.html)
