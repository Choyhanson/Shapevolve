"""Adjusters that modify the source image during evolution, but are undone for the final product."""

from math import log2

import numpy as np


def _dark_adjust_template(original_image, parameters):
    """A template for a function that logarithmically brightens dark parts of an image in numpy array form.

    :param original_image: The original image.
    :param parameters: Brightening parameters.
    :type original_image: ndarray
    :type parameters: List[Union[float, int]
    :return: An adjusted image.
    :rtype: ndarray
    """
    adjusted_image = original_image.copy()
    adjusted_image = adjusted_image + parameters[0]
    adjusted_image = np.log(adjusted_image) / np.log(parameters[1])
    adjusted_image = adjusted_image * parameters[2]
    adjusted_image = adjusted_image + parameters[3]
    adjusted_image = np.rint(adjusted_image).astype(np.uint8)
    return adjusted_image


def _dark_unadjust_template(adjusted_image, parameters):
    """A template for a function that reverses an logarithmic adjustment that had originally brightened the image.

    :param adjusted_image: The adjusted image.
    :param parameters: Brightening parameters.
    :type adjusted_image: ndarray
    :type parameters: List[Union[float, int]
    :return: The image with the adjustment reversed.
    :rtype: ndarray
    """
    original_image = adjusted_image.copy()
    original_image = original_image - parameters[3]
    original_image = original_image / parameters[2]
    original_image = np.exp2(log2(parameters[1]) * original_image)
    original_image = original_image - parameters[0]
    original_image = np.rint(original_image).astype(np.uint8)
    return original_image


_STRONG_DARK_ADJUST_PARAMETERS = [17.1976, 256, 512, -262.665]


def strong_dark_adjust(original_image):
    """A function that applies a strong brightening filter to a dark image.

    :param original_image: The original image.
    :type original_image: ndarray
    :return: The image with the adjustment applied.
    :rtype: ndarray
    """
    global _STRONG_DARK_ADJUST_PARAMETERS
    return _dark_adjust_template(original_image, _STRONG_DARK_ADJUST_PARAMETERS)


def strong_dark_unadjust(adjusted_image):
    """A function that reverses a strong brightening filter to a dark image.

    :param adjusted_image: The original image.
    :type adjusted_image: ndarray
    :return: The image with the adjustment applied.
    :rtype: ndarray
    """
    global _STRONG_DARK_ADJUST_PARAMETERS
    return _dark_unadjust_template(adjusted_image, _STRONG_DARK_ADJUST_PARAMETERS)


_WEAK_DARK_ADJUST_PARAMETERS = [52.5086, 256, 800, -571.448]


def weak_dark_adjust(original_image):
    """A function that applies a weak brightening filter to a dark image.

    :param original_image: The original image.
    :type original_image: ndarray
    :return: The image with the adjustment applied.
    :rtype: ndarray
    """
    global _WEAK_DARK_ADJUST_PARAMETERS
    return _dark_adjust_template(original_image, _WEAK_DARK_ADJUST_PARAMETERS)


def weak_dark_unadjust(adjusted_image):
    """A function that reverses a strong brightening filter to a dark image.

    :param adjusted_image: The original image.
    :type adjusted_image: ndarray
    :return: The image with the adjustment applied.
    :rtype: ndarray
    """
    global _WEAK_DARK_ADJUST_PARAMETERS
    return _dark_unadjust_template(adjusted_image, _WEAK_DARK_ADJUST_PARAMETERS)


"""Adjuster dictionaries. The adjust function must have "adjust" as its key, and the unadjust function
   must have "unadjust" as its key. All adjusters must follow this format."""

WEAK_DARK_ADJUSTER = {"adjust": weak_dark_adjust, "unadjust": weak_dark_unadjust}
STRONG_DARK_ADJUSTER = {"adjust": strong_dark_adjust, "unadjust": strong_dark_unadjust}
