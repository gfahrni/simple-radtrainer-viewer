# === screens/dicom_screen.py ===

import os  # import the OS module for file/folder operations
from kivy.app import App  # import App class to access the running app
from kivy.uix.screenmanager import Screen  # import Screen to create Kivy screens

# Import custom modules for DICOM handling
from dicom_viewer.series_loader import load_sorted_series  # function to load DICOM files in order
from dicom_viewer.image_processor import load_dicom_image  # function to convert DICOM file to image
from dicom_viewer.texture_utils import pil_to_texture  # function to convert PIL image to Kivy texture
from dicom_viewer.viewer_state import ViewerState  # class to keep track of images and current slice
from dicom_viewer.mouse_controller import MouseController  # class to handle mouse/scroll interactions


class DicomScreen(Screen):  # define the DicomScreen class, inherits from Kivy Screen

    def __init__(self, **kwargs):  # constructor called when creating the screen
        """
        Initialize the DicomScreen.

        - state: keeps track of the loaded images and current index.
        - mouse: handles mouse interactions like right-click and scroll.
        """
        super().__init__(**kwargs)  # call parent constructor to initialize the Screen properly
        self.state = ViewerState()  # create a ViewerState object to store images and current index
        self.mouse = MouseController()  # create a MouseController object to handle mouse input

    # -------------------------------
    #   MOUSE INPUT HANDLING
    # -------------------------------

    def on_image_touch_down(self, widget, touch):  # called when user presses down on the image
        """
        Called when the user presses down on the image.

        Handles:
        - Mouse scroll: navigate slices (up/down)
        - Right-click: stored for drag actions
        """
        res = self.mouse.touch_down(widget, touch)  # delegate the event to MouseController

        if res == 'scrolldown':  # if user scrolled down
            self.next_image()  # go to next image slice
        elif res == 'scrollup':  # if user scrolled up
            self.previous_image()  # go to previous image slice

        return True  # consume the touch event so it doesn't propagate further

    def on_image_touch_move(self, widget, touch):  # called when user moves mouse/finger on the image
        """
        Called when the user moves the mouse/finger on the image.

        Handles dragging with right-click to navigate slices vertically.
        """
        res = self.mouse.touch_move(widget, touch)  # delegate the move event to MouseController

        if res == "up":  # if dragging moved up
            self.previous_image()  # go to previous image slice
        elif res == "down":  # if dragging moved down
            self.next_image()  # go to next image slice

        return True  # consume the event

    def on_image_touch_up(self, widget, touch):  # called when user releases mouse/finger
        """
        Called when the user releases the mouse/finger.

        Ends right-click drag actions.
        """
        self.mouse.touch_up(touch)  # inform MouseController that touch ended
        return True  # consume the event

    # -------------------------------
    #   SLICE NAVIGATION
    # -------------------------------

    def next_image(self):  # move to next DICOM slice
        """
        Move to the next DICOM slice.

        Updates the displayed image if index changes.
        """
        if self.state.set_index(self.state.current_index + 1):  # increase index if possible
            self.update_image()  # refresh image on screen

    def previous_image(self):  # move to previous DICOM slice
        """
        Move to the previous DICOM slice.

        Updates the displayed image if index changes.
        """
        if self.state.set_index(self.state.current_index - 1):  # decrease index if possible
            self.update_image()  # refresh image on screen

    def on_slider_change(self, slider, value):  # called when slider value changes
        """
        Called when the slice slider is moved.

        Converts the slider value to the correct slice index
        and updates the displayed image.
        """
        idx = self.state.count() - 1 - int(value)  # convert slider value to image index (invert slider)
        if self.state.set_index(idx):  # set new index if valid
            self.update_image()  # refresh image

    # -------------------------------
    #     LOADING SERIES
    # -------------------------------

    def on_pre_enter(self):  # called automatically before the screen is displayed
        """
        Called before the screen is displayed.

        - Loads the selected DICOM series from the dataset folder.
        - Converts each image to a texture and stores it in state.
        - Updates the slider max value and displays the first image.
        """
        folder = App.get_running_app().selected_file  # get selected folder from the app
        if not folder:  # if no folder selected
            print("No dataset selected.")  # print warning
            return  # exit early

        files = load_sorted_series(folder)  # load all DICOM files sorted by anatomical position

        self.state.reset()  # clear any previously loaded images

        for path in files:  # loop over each file path
            try:
                img = load_dicom_image(path)  # read DICOM file and convert to image
                tex = pil_to_texture(img)  # convert image to Kivy texture
                self.state.images.append(tex)  # add texture to state
            except Exception as e:  # catch errors (e.g., corrupted DICOM)
                print("Image error:", path, e)  # print error message

        if not self.state.images:  # if no images loaded
            print("No DICOM images loaded.")  # warn user
            return  # exit early

        self.ids.slice_slider.max = self.state.count() - 1  # set slider max value
        self.ids.slice_slider.value = self.state.count() - 1  # set slider to first slice (top)

        self.update_image()  # display first image

    # -------------------------------
    #       DISPLAY UPDATE
    # -------------------------------

    def update_image(self):  # update the displayed image
        """
        Updates the Kivy image widget with the currently selected slice texture.
        """
        tex = self.state.get_current_texture()  # get current slice texture
        if tex:  # if texture exists
            self.ids.dicom_image.texture = tex  # update Kivy Image widget
            # synchronize slider value with current index
            self.ids.slice_slider.value = self.state.count() - 1 - self.state.current_index  

    def go_back(self):  # switch back to main screen
        """
        Switches back to the main screen.
        """
        self.manager.current = "main"  # tell ScreenManager to show main screen
