import numpy as np
import cv2 as cv


class GrabCutApp:
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

        return self.img_out