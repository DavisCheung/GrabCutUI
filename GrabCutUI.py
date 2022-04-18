import numpy as np
import cv2 as cv


class GrabCutApp:
    def remove_black_bg(img):
        temp_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # Convert to GRAY
        _, alpha = cv.threshold(temp_img, 0, 255, cv.THRESH_BINARY)
        b, g, r = cv.split(img)  # Split b, g, and r channels
        rgba = [b, g, r, alpha]  # Splice in the alpha channel
        img_out = cv.merge(rgba, 4)  # Convert to img w/ alpha channel (currently just a list)
        return img_out

    def run(self, img_in, sel_in):
        # Sets image to the selected file; initializes a blank mask
        self.img_in = img_in  # Copy of image for selection use
        self.mask = np.zeros(self.img_in.shape[:2], np.uint8)
        self.img_out = np.zeros(self.img_in.shape, np.uint8)

        # Initialize selection
        self.selection = sel_in

        # print(self.selection)

        try:
            # Internally-used arrays in algorithm
            bg_model = np.zeros((1, 65), np.float64)
            fg_model = np.zeros((1, 65), np.float64)

            iter = 5  # Number of algorithm iterations desired

            cv.grabCut(
                self.img_in,
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

        # Makes a new mask from the grabCut mask
        # Generates output image via matrix mult. w/ mask
        self.mask2 = np.where((self.mask == 2) | (self.mask == 0), 0, 1).astype("uint8")
        self.img_out = self.img_in * self.mask2[:, :, np.newaxis]

        self.img_out = self.remove_black_bg(self.img_out)  # Remove black background



        return self.img_out