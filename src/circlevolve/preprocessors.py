from PIL import ImageFilter, ImageEnhance


def smooth_preprocess(image):
    smooth_filter = ImageFilter.SMOOTH_MORE
    return image.filter(smooth_filter).filter(smooth_filter).filter(smooth_filter)


def saturate_preprocess(image):
    saturate_enhancer = ImageEnhance.Color(image)
    return saturate_enhancer.enhance(1.5)


def desaturate_preprocess(image):
    desaturate_enhancer = ImageEnhance.Color(image)
    return desaturate_enhancer.enhance(0.5)


def contrast_preprocess(image):
    contrast_enhancer = ImageEnhance.Contrast(image)
    return contrast_enhancer.enhance(1.5)


def decontrast_preprocess(image):
    decontrast_enhancer = ImageEnhance.Contrast(image)
    return decontrast_enhancer.enhance(0.5)


def brighten_preprocess(image):
    brighten_enhancer = ImageEnhance.Brightness(image)
    return brighten_enhancer.enhance(1.5)


def debrighten_preprocess(image):
    debrighten_enhancer = ImageEnhance.Brightness(image)
    return debrighten_enhancer.enhance(0.5)
