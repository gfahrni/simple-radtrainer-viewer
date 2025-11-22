# === dicom_viewer/series_loader.py ===
# This file contains functions to load DICOM series from a folder,
# read their anatomical positions, and sort them cranio-caudally
# (head → foot) for correct display order.

import os  # import OS module to work with filesystem paths
import pydicom  # import pydicom to read DICOM files
from .orientation import get_anatomical_position  # import function to get Z position of a slice

def load_sorted_series(folder_path):
    """
    Load all DICOM files in a folder, sort them by anatomical position,
    and return the file paths in cranio-caudal order.

    Parameters:
    - folder_path: path to the folder containing DICOM files

    Returns:
    - List of file paths sorted from top (head) to bottom (foot)
    """

    dicom_files = []  # list to store tuples: (position, file_path)

    # Loop over each file in the folder
    for f in os.listdir(folder_path):
        # Only consider files with DICOM extensions
        if f.lower().endswith(('.dcm', '.dicom')):
            path = os.path.join(folder_path, f)  # get full path of the file

            try:
                # Read the DICOM header only (stop_before_pixels=True avoids loading image data)
                ds = pydicom.dcmread(path, stop_before_pixels=True)
                # Get the anatomical Z position (or fallback to InstanceNumber)
                pos = get_anatomical_position(ds)
                # Store a tuple of (position, path) to sort later
                dicom_files.append((pos, path))
            except Exception as e:
                # Print a warning if the DICOM header cannot be read
                print("Header read error:", path, e)

    # Sort the files based on anatomical position (cranial → caudal)
    dicom_files.sort(key=lambda x: x[0])  # sort by the first element of the tuple (position)

    # Return a list of only the file paths, now sorted in the correct order
    return [path for _, path in dicom_files]
