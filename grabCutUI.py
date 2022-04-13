import tkinter
import numpy as np
import cv2 as cv
from tkinter import filedialog
from tkinter import *


class GrabCutApp():
    GREEN = [0,255,0]

    # Initialization
    selection = (0,0,1,1)    # Rectangle for selectiong
    selecting = False        # Flag for selection

    # User-drawn rectangle for selection
    def select_object(self, event, x, y, flags, param):

        if event == cv.EVENT_LBUTTONDOWN:
            self.selecting = True
            self.xPos = x
            self.yPos = y
        
        elif event == cv.EVENT_MOUSEMOVE:
            if self.selecting == True:
                self.imgIn = self.refImg.copy()
                cv.rectangle(self.imgIn, (self.xPos, self.yPos), (x, y), self.GREEN, 1)
                self.selection = (min(self.xPos, x), min(self.yPos, y), abs(self.xPos - x), abs(self.yPos - y))


        elif event == cv.EVENT_LBUTTONUP:
            self.selecting = False
            cv.rectangle(self.imgIn, (self.xPos, self.yPos), (x, y), self.GREEN, 1)
            self.selection = (min(self.xPos, x), min(self.yPos, y), abs(self.xPos - x), abs(self.yPos - y))

    # The app itself
    def run(self):
        print("Greetings! Please select an image.")
        print("Note that large images may be hard to edit with this app.\n")

        # File selection
        self.root = tkinter.Tk()
        self.imgname = filedialog.askopenfilename(parent=self.root,
            initialdir="./Test_Images",
            title='Please select an image', 
            filetypes=[("Images", ["*.png", "*.jpg", "*.jpeg"]), ("all files", "*.*")]
        )

        # Sets image to the selected file; initializes a blank mask of same dimensions
        self.imgIn = cv.imread(self.imgname) # Copy of image to use in selection
        self.mask = np.zeros(self.imgIn.shape[:2],np.uint8)
        self.imgOut = np.zeros(self.imgIn.shape,np.uint8)

        self.refImg = self.imgIn.copy() # Copy of image for algorithm use

        # Windows for Image Selection & Preview
        cv.namedWindow("Image Selection")
        cv.namedWindow("Preview")
        cv.setMouseCallback("Image Selection", self.select_object)

        print("Please draw a rectangle around the object you wish to cut-out.")
        print("After you are finished with your selection, please press enter.\n")

        # Program loop
        while(1):
            cv.imshow("Image Selection", self.imgIn)
            cv.imshow("Preview", self.imgOut)
            input = cv.waitKey(1) # Note. Since the keycode used is assumed to be Windows, this will only work on Windows

            if (input == 13): # ENTER key on Windows
                try:
                    # Internally used arrays in algorithm
                    bgdModel = np.zeros((1,65),np.float64)
                    fgdModel = np.zeros((1,65),np.float64)

                    # Number of algorithm iterations desired
                    iter = 5

                    cv.grabCut(self.refImg,self.mask,self.selection,bgdModel,fgdModel,iter,cv.GC_INIT_WITH_RECT)
                except:
                    import traceback
                    traceback.print_exc()


            mask2 = np.where((self.mask==2)|(self.mask==0),0,1).astype('uint8')
            self.imgOut = self.refImg*mask2[:,:,np.newaxis]

            if (input == 27): # ESC on Windows
                break

        # Outputs to local directory as "cutImage.png"
        cv.imwrite("./cutImage.png", self.imgOut)


GrabCutApp().run()
cv.destroyAllWindows()