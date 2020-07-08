from pathlib import Path

import cv2
from matplotlib.pyplot import draw, pause, imshow

from adjusters import unadjust


def convert_RGB_to_BGR(color):  # converts from RGB (colorthief colors) to BGR format (opencv2 colors)
    return color[2], color[1], color[0]


def show_image(image, display=None, adjusters=None):  # Shows the image

    if adjusters is None:
        adjusters = []

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


def get_image_path(name, directory):
    return str(Path(__file__).absolute().parent) + "\\" + directory + "\\" + name
