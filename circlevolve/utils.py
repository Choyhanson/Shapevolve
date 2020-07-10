"""Utility methods."""

from pathlib import Path

import cv2
from PIL import Image
from colorthief import ColorThief
from matplotlib.pyplot import draw, pause, imshow, title, axis


def convert_RGB_to_BGR(color):
    """Converts a RGB color to a BGR color.

    :param color: The RGB color.
    :type color: Tuple[int, int, int]
    :return: The corresponding BGR color.
    :rtype: Tuple[int, int, int]
    """
    return color[2], color[1], color[0]


def show_image(image, generation, display=None, adjusters=None):
    """Uses matplotlib to show an image.

    :param image: The image to show.
    :param generation: What generation the image corresponds to.
    :param display: The window the image should display on.
    :param adjusters: Any adjusters that should be reversed for the image.
    :type image: ndarray
    :type generation: int
    :type display: AxesImage
    :type adjusters: Dict[str, Callable]
    :return: The window where the image was displayed.
    :rtype: AxesImage
    """
    if adjusters is None:
        adjusters = []

    axis("off")
    title(f"Generation {generation}", fontsize=12)

    restored_image = unadjust(image, adjusters)
    restored_image = cv2.cvtColor(restored_image, cv2.COLOR_BGR2RGB)
    if display is None:
        display = imshow(restored_image)
    else:
        display.set_data(restored_image)

    draw()
    pause(0.01)
    return display


def get_rescale_ratio(image, target):
    """Gets the required ratio to rescale an image to a target resolution

    :param image: An image to resize.
    :param target: The target resolution to resize to.
    :type image: Image
    :type target: int
    :return: The min of the ratio between the target resolution and the image's smallest dimension, and 1.
    :rtype: float
    """
    width = image.width
    height = image.height

    if width <= target or height <= target:
        return 1

    ratio = target / min(width, height)
    return ratio


def adjust(original_image, adjusters):
    """Adjusts an image based on adjusters.

    :param original_image: The original image before adjustments.
    :param adjusters: Adjusters to apply.
    :type original_image: ndarray
    :type adjusters: List[Dict[str, Callable]]
    :return: The adjusted image.
    :rtype: ndarray
    """
    if not adjusters:
        return original_image

    adjustments = [adjuster['adjust'] for adjuster in adjusters]
    adjusted_image = original_image.copy()

    for adjustment in adjustments:
        adjusted_image = adjustment(adjusted_image)

    return adjusted_image


def unadjust(adjusted_image, adjusters):
    """Reverses an adjustment on an image based on adjusters.

    :param adjusted_image: The image after adjustments.
    :param adjusters: Adjusters to reverse.
    :type adjusted_image: ndarray
    :type adjusters: List[Dict[str, Callable]]
    :return: The unadjusted image.
    :rtype: ndarray
    """
    if not adjusters:
        return adjusted_image

    unadjustments = reversed([adjuster['unadjust'] for adjuster in adjusters])
    original_image = adjusted_image.copy()

    for unadjustment in unadjustments:
        original_image = unadjustment(original_image)

    return original_image


def get_image_path(name, directory):
    """Gets the path of an image based on a directory in the script's folder and a name.

    :param name: The name of the image.
    :param directory: The directory name, in the same folder as this script.
    :type name: str
    :type directory: str
    :return: The filepath.
    :rtype: string
    """
    return str(Path(__file__).absolute().parent) + "\\" + directory + "\\" + name


class ColorThiefFromImage(ColorThief):
    """This class extends ColorThief to support providing images as-is instead of filenames."""

    # noinspection PyMissingConstructor
    def __init__(self, image):
        """Builds the ColorThief object with an image field.

        :param image: The image to build colors from.
        :type image: Image
        """
        self.image = image


def get_image(path):
    """A shortcut to get an image from a filepath.

    :param path: The filepath of the image.
    :type path: str
    :return: The image object.
    :rtype: Image
    """
    return Image.open(path)
