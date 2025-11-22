# === dicom_viewer/orientation.py ===
# This file contains functions to handle DICOM image orientation.
# It ensures that slices are displayed in the correct anatomical view,
# accounting for patient positioning and image orientation metadata.

import numpy as np  # import numpy for array manipulation

def get_anatomical_position(ds):
    """
    Get the anatomical Z position of a DICOM slice.

    Parameters:
    - ds: a pydicom Dataset object (DICOM file header)

    Returns:
    - Z position (float) of the slice
    - Falls back to InstanceNumber if ImagePositionPatient is missing
    """
    try:
        # Try to get the Z coordinate from ImagePositionPatient
        ipp = ds.ImagePositionPatient
        if ipp:
            return float(ipp[2])  # Z position in mm
    except:
        pass  # ignore errors if the tag is missing

    try:
        # Fallback: use InstanceNumber if ImagePositionPatient not available
        return float(ds.InstanceNumber)
    except:
        # If all else fails, return 0
        return 0

def apply_radiological_orientation(arr, ds):
    """
    Correct the image array according to the radiological orientation.

    Parameters:
    - arr: numpy array representing the image pixels
    - ds: pydicom Dataset object

    Returns:
    - Oriented numpy array suitable for display
    """

    try:
        iop = ds.ImageOrientationPatient  # get orientation metadata
        if not iop:
            return arr  # no orientation info, return original array

        # Orientation vectors
        row = np.array(iop[:3])  # direction of image rows
        col = np.array(iop[3:6])  # direction of image columns
        norm = np.cross(row, col)  # normal vector to the image plane

        flip_h = False  # flag to flip image horizontally
        flip_v = False  # flag to flip image vertically

        # Determine if horizontal flip is needed
        if abs(row[1]) > 0.7 and row[1] > 0:
            flip_h = True

        # Determine if vertical flip is needed
        if abs(col[1]) > 0.7 and col[1] > 0:
            flip_v = True

        # Additional check using the normal vector
        if abs(norm[2]) > 0.7 and norm[2] > 0:
            flip_v = True

        # Apply vertical flip if necessary
        if flip_v:
            arr = np.flipud(arr)  # flip upside-down

        # Apply horizontal flip if necessary
        if flip_h:
            arr = np.fliplr(arr)  # flip left-right

    except Exception:
        # If anything fails, fallback to a vertical flip
        arr = np.flipud(arr)

    return arr  # return the oriented image array
