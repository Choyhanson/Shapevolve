from pathlib import Path

import cv2
from colorthief import ColorThief
from matplotlib.pyplot import draw, pause, imshow, title, axis


def convert_RGB_to_BGR(color):  # converts from RGB (colorthief colors) to BGR format (opencv2 colors)
    return color[2], color[1], color[0]


def show_image(image, generation, display=None, adjusters=None):  # Shows the image

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


def get_rescale_ratio(image, target):  # Gets a rescale ratio based on an image and a target resolution
    # Target: 250x250
    width = image.width
    height = image.height

    if width <= target or height <= target:
        return 1

    ratio = target / min(width, height)
    return ratio


def adjust(original_image, adjusters):
    if not adjusters:
        return original_image

    adjustments = [adjuster['adjust'] for adjuster in adjusters]
    adjusted_image = original_image.copy()

    for adjustment in adjustments:
        adjusted_image = adjustment(adjusted_image)

    return adjusted_image


def unadjust(adjusted_image, adjusters):
    if not adjusters:
        return adjusted_image

    unadjustments = reversed([adjuster['unadjust'] for adjuster in adjusters])
    original_image = adjusted_image.copy()

    for unadjustment in unadjustments:
        original_image = unadjustment(original_image)

    return original_image


def get_image_path(name, directory):
    return str(Path(__file__).absolute().parent) + "\\" + directory + "\\" + name


class ColorThiefFromImage(ColorThief):  # Extend ColorThief to support providing images as-is instead of filenames
    # noinspection PyMissingConstructor
    def __init__(self, image):
        self.image = image
