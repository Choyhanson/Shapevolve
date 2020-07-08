from PIL import ImageFilter


def smooth_preprocess(image):
    smooth_filter = ImageFilter.SMOOTH_MORE
    return image.filter(smooth_filter).filter(smooth_filter).filter(smooth_filter)


def no_preprocess(image):
    return image
