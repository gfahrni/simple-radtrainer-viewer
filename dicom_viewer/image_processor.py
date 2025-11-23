# === dicom_viewer/image_processor.py ===
# This file contains functions to load DICOM images and convert them
# into a format suitable for display in the Kivy app (PIL Image objects).

import pydicom
import numpy as np
from PIL import Image as PILImage
from .orientation import apply_radiological_orientation
from .dicom_windowing import apply_dicom_windowing  # Import the new windowing function

def load_dicom_image(path):
    """
    Load a single DICOM file and convert it to a PIL Image.

    Parameters:
    - path: path to the DICOM file

    Returns:
    - PIL Image object with corrected orientation and proper windowing
    """

    # Read the DICOM file
    ds = pydicom.dcmread(path)

    # Convert pixel data to float32 for processing
    arr = ds.pixel_array.astype(np.float32)

    # Apply DICOM windowing using the new robust function
    arr = apply_dicom_windowing(arr, ds)

    # Apply radiological orientation
    arr = apply_radiological_orientation(arr, ds)

    # Convert the numpy array to a PIL Image
    return PILImage.fromarray(arr)