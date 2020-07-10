"""Defines error metrics that can be used to evaluate similarity between two images."""

import skimage.metrics  # For similarity measurement


def mean_squared_error(image, source):
    """Calculates the mean squared error between two images.

    :param image: The constructed image.
    :param source: The original image.
    :type image: ndarray
    :type source: ndarray
    :return: The mean squared error between the two images.
    :rtype: float
    """
    return skimage.metrics.mean_squared_error(image, source)


def structural_similarity_error(image, source):
    """Calculates the opposite of the structural similarity between two images.

    :param image: The constructed image.
    :param source: The original image.
    :type image: ndarray
    :type source: ndarray
    :return: The opposite of the structural similarity between the two images.
    :rtype: float
    """
    return -1 * skimage.metrics.structural_similarity(image, source, multichannel=True)
