from math import log2

import numpy as np


def _dark_adjust_template(original_image, parameters):
    adjusted_image = original_image.copy()
    adjusted_image = adjusted_image + parameters[0]
    adjusted_image = np.log(adjusted_image) / np.log(parameters[1])
    adjusted_image = adjusted_image * parameters[2]
    adjusted_image = adjusted_image + parameters[3]
    adjusted_image = np.rint(adjusted_image).astype(np.uint8)
    return adjusted_image


def _dark_unadjust_template(adjusted_image, parameters):
    original_image = adjusted_image.copy()
    original_image = original_image - parameters[3]
    original_image = original_image / parameters[2]
    original_image = np.exp2(log2(parameters[1]) * original_image)
    original_image = original_image - parameters[0]
    original_image = np.rint(original_image).astype(np.uint8)
    return original_image


_STRONG_DARK_ADJUST_PARAMETERS = [17.1976, 256, 512, -262.665]


def strong_dark_adjust(original_image):
    global _STRONG_DARK_ADJUST_PARAMETERS
    return _dark_adjust_template(original_image, _STRONG_DARK_ADJUST_PARAMETERS)


def strong_dark_unadjust(adjusted_image):
    global _STRONG_DARK_ADJUST_PARAMETERS
    return _dark_unadjust_template(adjusted_image, _STRONG_DARK_ADJUST_PARAMETERS)


_WEAK_DARK_ADJUST_PARAMETERS = [52.5086, 256, 800, -571.448]


def weak_dark_adjust(original_image):
    global _WEAK_DARK_ADJUST_PARAMETERS
    return _dark_adjust_template(original_image, _WEAK_DARK_ADJUST_PARAMETERS)


def weak_dark_unadjust(adjusted_image):
    global _WEAK_DARK_ADJUST_PARAMETERS
    return _dark_unadjust_template(adjusted_image, _WEAK_DARK_ADJUST_PARAMETERS)


WEAK_DARK_ADJUSTER = {"adjust": strong_dark_adjust, "unadjust": strong_dark_unadjust}
STRONG_DARK_ADJUSTER = {"adjust": strong_dark_adjust, "unadjust": strong_dark_unadjust}
