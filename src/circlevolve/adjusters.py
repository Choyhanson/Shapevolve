from math import log2

import numpy as np


def default_adjust(image):
    return image


def dark_adjust(original_image):
    adjust_parameters = [17.1976, 256, 512, -262.665]

    adjusted_image = original_image.copy()
    adjusted_image = adjusted_image + adjust_parameters[0]
    adjusted_image = np.log(adjusted_image) / np.log(adjust_parameters[1])
    adjusted_image = adjusted_image * adjust_parameters[2]
    adjusted_image = adjusted_image + adjust_parameters[3]
    adjusted_image = np.rint(adjusted_image).astype(np.uint8)
    return adjusted_image


def dark_unadjust(adjusted_image):
    adjust_parameters = [17.1976, 256, 512, -262.665]

    original_image = adjusted_image.copy()
    original_image = original_image - adjust_parameters[3]
    original_image = original_image / adjust_parameters[2]
    original_image = np.exp2(log2(adjust_parameters[1]) * original_image)
    original_image = original_image - adjust_parameters[0]
    original_image = np.rint(original_image).astype(np.uint8)
    return original_image


NO_ADJUSTER = {"adjust": default_adjust, "unadjust": default_adjust}
DARK_ADJUSTER = {"adjust": dark_adjust, "unadjust": dark_unadjust}
