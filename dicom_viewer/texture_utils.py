# === dicom_viewer/texture_utils.py ===
# This file contains helper functions to convert images from PIL format
# into Kivy textures, which can be displayed in Kivy Image widgets.

from kivy.graphics.texture import Texture  # import Kivy Texture class

def pil_to_texture(pil_image):
    """
    Convert a PIL Image to a Kivy Texture.

    Parameters:
    - pil_image: a PIL Image object (grayscale or RGB)

    Returns:
    - Kivy Texture object that can be assigned to an Image widget
    """

    # Ensure the image is in grayscale ('L' mode)
    pil_image = pil_image.convert('L')  # 'L' = 8-bit pixels, black and white

    # Convert the PIL image data into a raw bytes buffer
    raw = pil_image.tobytes()  # get pixel data as bytes

    # Create a new Kivy texture object with the same size as the image
    # colorfmt='luminance' indicates a grayscale image
    tex = Texture.create(size=pil_image.size, colorfmt='luminance')

    # Copy the raw bytes into the texture
    # bufferfmt='ubyte' means each pixel is 1 byte (0-255)
    tex.blit_buffer(raw, colorfmt='luminance', bufferfmt='ubyte')

    # Return the Kivy texture so it can be displayed in the UI
    return tex
