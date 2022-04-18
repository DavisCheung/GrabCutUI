import numpy as np
import cv2 as cv


class GrabCutApp:
    def run(self, img_in, sel_in):
        # Sets image to the selected file; initializes a blank mask
        self.img_in = img_in  # Copy of image for selection use
        self.mask = np.zeros(self.img_in.shape[:2], np.uint8)
        self.img_out = np.zeros(self.img_in.shape, np.uint8)

        self.ref_img = self.img_in.copy()  # Copy of image for algorithm use

        # Initialize selection
        self.selection = sel_in

        # print(self.selection)

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

        # Makes a new mask from the grabCut mask
        # Generates output image via matrix mult. w/ mask
        self.mask2 = np.where((self.mask == 2) | (self.mask == 0), 0, 1).astype("uint8")
        self.img_out = self.ref_img * self.mask2[:, :, np.newaxis]

        return self.img_out

    """ Python script version w/ selection code
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
                cv.rectangle(
                    self.img_in, (self.x_pos, self.y_pos), (x, y), self.GREEN, 1
                )
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

        # Old File selection
        self.root = tkinter.Tk()
        self.img_name = filedialog.askopenfilename(
            parent=self.root,
            initialdir="./Test_Images",
            title="Please select an image",
            filetypes=[("Images", ["*.png", "*.jpg", "*.jpeg"]), ("all files", "*.*")],
        )

        # Sets image to the selected file; initializes a blank mask
        self.img_in = img_in  # Copy of image for selection use
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
    """
