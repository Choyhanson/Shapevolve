from PIL import ImageFilter, ImageEnhance


def smooth_preprocess(image):
    """Smooths an image.

    :param image: The image to smooth.
    :type image: Image
    :return: The smoothed image.
    :rtype: Image
    """
    smooth_filter = ImageFilter.SMOOTH_MORE
    return image.filter(smooth_filter).filter(smooth_filter).filter(smooth_filter)


def saturate_preprocess(image):
    """Saturates an image.

    :param image: The image to saturate.
    :type image: Image
    :return: The saturated image.
    :rtype: Image
    """
    saturate_enhancer = ImageEnhance.Color(image)
    return saturate_enhancer.enhance(1.5)


def desaturate_preprocess(image):
    """Desaturates an image.

    :param image: The image to desaturate.
    :type image: Image
    :return: The desaturated image.
    :rtype: Image
    """
    desaturate_enhancer = ImageEnhance.Color(image)
    return desaturate_enhancer.enhance(0.5)


def contrast_preprocess(image):
    """Increases contrast of an image.

    :param image: The image to process.
    :type image: Image
    :return: The processed image.
    :rtype: Image
    """
    contrast_enhancer = ImageEnhance.Contrast(image)
    return contrast_enhancer.enhance(1.5)


def decontrast_preprocess(image):
    """Decreases contrast of an image.

    :param image: The image to process.
    :type image: Image
    :return: The processed image.
    :rtype: Image
    """
    decontrast_enhancer = ImageEnhance.Contrast(image)
    return decontrast_enhancer.enhance(0.5)


def brighten_preprocess(image):
    """Increases brightness of an image.

    :param image: The image to process.
    :type image: Image
    :return: The processed image.
    :rtype: Image
    """
    brighten_enhancer = ImageEnhance.Brightness(image)
    return brighten_enhancer.enhance(1.5)


def debrighten_preprocess(image):
    """Decreases brightness of an image.

    :param image: The image to process.
    :type image: Image
    :return: The processed image.
    :rtype: Image
    """
    debrighten_enhancer = ImageEnhance.Brightness(image)
    return debrighten_enhancer.enhance(0.5)
