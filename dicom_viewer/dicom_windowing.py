"""
DICOM Windowing Module

This module handles DICOM window center and width extraction and application.
It provides robust functions to read windowing parameters from DICOM files
regardless of how they are stored (single value vs multi-value format).
"""

import pydicom
import numpy as np


def get_window_parameters(ds):
    """
    Extract window center and width from DICOM dataset.
    
    Handles all DICOM formats including string values with backslashes.
    """
    window_center = None
    window_width = None
    
    def parse_dicom_value(value):
        """Parse DICOM values that can be numbers, lists, or strings with backslashes"""
        if value is None:
            return None
            
        # If it's already a number
        if isinstance(value, (int, float)):
            return float(value)
        
        # If it's a multi-value element (list/tuple)
        if hasattr(value, '__len__') and not isinstance(value, str):
            if len(value) > 0:
                return float(value[0])  # Take first value
            return None
        
        # If it's a string (like "00040\00040")
        if isinstance(value, str):
            # Split by backslash and take first part
            parts = value.split('\\')
            if parts and parts[0].strip():
                try:
                    return float(parts[0])
                except (ValueError, TypeError):
                    pass
        
        # Final attempt: direct conversion
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    # Extract Window Center (0028,1050)
    if (0x0028, 0x1050) in ds:
        center_element = ds[0x0028, 0x1050]
        if hasattr(center_element, 'value'):
            window_center = parse_dicom_value(center_element.value)
            #print(f"DEBUG WindowCenter - Raw: {center_element.value}, Parsed: {window_center}")
    
    # Extract Window Width (0028,1051)
    if (0x0028, 0x1051) in ds:
        width_element = ds[0x0028, 0x1051]
        if hasattr(width_element, 'value'):
            window_width = parse_dicom_value(width_element.value)
            #print(f"DEBUG WindowWidth - Raw: {width_element.value}, Parsed: {window_width}")

    #print(f"DICOM Windowing - Final: Center={window_center}, Width={window_width}")
    return window_center, window_width

def apply_dicom_windowing(image_array, ds):
    """
    Apply DICOM windowing to a numpy array using parameters from DICOM metadata.
    """
    # Get window parameters from DICOM metadata
    window_center, window_width = get_window_parameters(ds)
    
    # DEBUG: Check for CT rescale parameters
    has_rescale = hasattr(ds, 'RescaleSlope') and hasattr(ds, 'RescaleIntercept')
    #print(f"DEBUG - Has rescale params: {has_rescale}")
    if has_rescale:
        #print(f"DEBUG - RescaleSlope: {ds.RescaleSlope}, RescaleIntercept: {ds.RescaleIntercept}")
        # APPLY RESCALE - CRITICAL FOR CT!
        image_array = image_array * float(ds.RescaleSlope) + float(ds.RescaleIntercept)
    
    #print(f"DEBUG - Raw array range: [{np.min(image_array):.1f}, {np.max(image_array):.1f}]")
    
    # If window parameters found, apply DICOM windowing
    if window_center is not None and window_width is not None:
        # Calculate window bounds CORRECTLY
        window_min = window_center - window_width / 2
        window_max = window_center + window_width / 2
        
        #print(f"DEBUG - Window Center: {window_center}, Width: {window_width}")
        #print(f"DEBUG - Window Range: [{window_min:.1f}, {window_max:.1f}]")
        
        # Apply windowing with proper clipping and normalization
        windowed = np.clip(image_array, window_min, window_max)
        
        # Normalize to 0-255 range
        if window_max > window_min:
            windowed = (windowed - window_min) / (window_max - window_min) * 255
        else:
            windowed = np.zeros_like(image_array)
            
        result = np.clip(windowed, 0, 255).astype(np.uint8)
        
    else:
        # Fallback for CT without window parameters
        img_min = np.min(image_array)
        img_max = np.max(image_array)
        #print(f"DEBUG FALLBACK - Raw array range: [{img_min:.1f}, {img_max:.1f}]")
        
        if img_max > img_min:
            result = ((image_array - img_min) / (img_max - img_min) * 255).astype(np.uint8)
        else:
            result = np.zeros_like(image_array, dtype=np.uint8)
    
    #print(f"DEBUG - Final range: [{np.min(result)}, {np.max(result)}]")
    return result