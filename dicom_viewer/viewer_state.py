# === dicom_viewer/viewer_state.py ===
# This file defines a class to keep track of the current DICOM series
# and the currently displayed slice. Essentially, it stores all images
# (as Kivy textures) and provides methods to navigate through them.

class ViewerState:
    """
    Class to manage the state of the DICOM viewer.

    Responsibilities:
    - Store all loaded image textures
    - Keep track of the currently displayed slice
    - Provide methods to navigate through slices
    """

    def __init__(self):
        """
        Initialize the ViewerState object.

        Attributes:
        - images: list of Kivy textures representing each DICOM slice
        - current_index: integer index of the currently displayed image
        """
        self.images = []  # empty list to store image textures
        self.current_index = 0  # start at the first slice by default

    def reset(self):
        """
        Reset the viewer state.

        Clears all loaded images and sets the current index back to 0.
        Useful when loading a new DICOM series.
        """
        self.images.clear()  # remove all textures from the list
        self.current_index = 0  # reset the current slice index

    def count(self):
        """
        Return the number of loaded images.

        Returns:
        - Integer count of images in self.images
        """
        return len(self.images)  # simply return the length of the images list

    def set_index(self, index):
        """
        Update the current slice index.

        Parameters:
        - index: the new slice index to display

        Returns:
        - True if the index was valid and updated
        - False if the index is out of range

        This ensures the viewer does not go beyond first/last slice.
        """
        if 0 <= index < len(self.images):  # check if index is within valid range
            self.current_index = index  # update current_index
            return True  # indicate success
        return False  # index was invalid, do not update

    def get_current_texture(self):
        """
        Get the texture of the currently displayed slice.

        Returns:
        - Kivy Texture object of the current image
        - None if no images are loaded

        This is used by DicomScreen to update the displayed image.
        """
        if self.images:  # check if there are any loaded images
            return self.images[self.current_index]  # return the texture at current_index
        return None  # no images loaded, return None
