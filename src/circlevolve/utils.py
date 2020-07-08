from pathlib import Path

import cv2
from matplotlib.pyplot import draw, pause, imshow

from adjusters import NO_ADJUSTER


def convert_RGB_to_BGR(color):  # converts from RGB (colorthief colors) to BGR format (opencv2 colors)
    return color[2], color[1], color[0]


def show_image(image, display=None,
               adjuster=NO_ADJUSTER):  # Shows the image
    restored_image = adjuster['unadjust'](image)
    restored_image = cv2.cvtColor(restored_image, cv2.COLOR_BGR2RGB)
    if display is None:
        display = imshow(restored_image)
    else:
        display.set_data(restored_image)

    draw()
    pause(0.01)
    return display


def add_circle(image, gene,
               palette):  # Adds a circle based on gene information onto an image using opencv2 blending modes.
    overlay = image.copy()
    cv2.circle(
        overlay,
        center=gene.center,
        radius=gene.radius,
        color=palette[gene.color],
        thickness=-1,
        lineType=cv2.LINE_AA  # add antialiasing
    )
    cv2.addWeighted(overlay, gene.alpha, image, 1 - gene.alpha, 0, image)


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
