# === dicom_viewer/image_processor.py ===
# This file contains functions to load DICOM images and convert them
# into a format suitable for display in the Kivy app (PIL Image objects).

import pydicom  # import pydicom to read DICOM files
import numpy as np  # import numpy for numerical operations
from PIL import Image as PILImage  # import PIL Image to manipulate images
from .orientation import apply_radiological_orientation  # import orientation correction function

def load_dicom_image(path):
    """
    Load a single DICOM file and convert it to a PIL Image.

    Parameters:
    - path: path to the DICOM file

    Returns:
    - PIL Image object with corrected orientation and normalized pixel values
    """

    # Read the DICOM file
    ds = pydicom.dcmread(path)  # ds is a pydicom Dataset object

    # Convert pixel data to float32 for processing
    arr = ds.pixel_array.astype(np.float32)  # original pixel data

    # -------------------------------
    # Normalize pixel values to 0-255
    # -------------------------------
    # Scale pixel values so the min becomes 0 and max becomes 255
    arr = (arr - np.min(arr)) / (np.max(arr) - np.min(arr)) * 255
    arr = arr.astype(np.uint8)  # convert to 8-bit unsigned integers

    # -------------------------------
    # Apply radiological orientation
    # -------------------------------
    # Corrects flipped or rotated images according to DICOM metadata
    arr = apply_radiological_orientation(arr, ds)

    # Convert the numpy array to a PIL Image
    return PILImage.fromarray(arr)  # return the PIL Image
