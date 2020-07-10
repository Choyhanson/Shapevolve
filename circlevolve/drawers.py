"""Defines functions that can be used to draw shapes on an image based on genetic information by the evolver class."""

import cv2


def add_circle(image, gene, palette):
    """Adds a circle to an image based on info from a gene.

    :param image: The base image to draw the circle on.
    :param gene: The gene that specifies how to draw the circle.
    :param palette: The color palette where colors are referenced from.
    :type image: ndarray
    :type gene: Gene
    :type palette: List[Tuple[int, int, int]]
    """
    overlay = image.copy()
    cv2.circle(
        overlay,
        center=gene.center,
        radius=gene.radius,
        color=palette[gene.color],
        thickness=-1,
        lineType=cv2.LINE_AA  # add anti-aliasing
    )
    draw_overlay(image, overlay, gene.alpha)


def add_square(image, gene, palette):
    """Adds a square to an image based on info from a gene.

    :param image: The base image to draw the square on.
    :param gene: The gene that specifies how to draw the square.
    :param palette: The color palette where colors are referenced from.
    :type image: ndarray
    :type gene: Gene
    :type palette: List[Tuple[int, int, int]]
    """
    overlay = image.copy()
    point1 = (gene.center[0] - gene.radius, gene.center[1] - gene.radius)
    point2 = (gene.center[0] + gene.radius, gene.center[1] + gene.radius)
    cv2.rectangle(
        overlay,
        point1,
        point2,
        color=palette[gene.color],
        thickness=-1,
        lineType=cv2.LINE_AA
    )
    draw_overlay(image, overlay, gene.alpha)


def draw_overlay(image, overlay, alpha):
    """Draws an overlay over an image at a specified alpha.

    :param image: The base image.
    :param overlay: The overlay image.
    :param alpha: The opacity, from 0 to 1.
    :type image: ndarray
    :type overlay: ndarray
    :type alpha: float
    """
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
