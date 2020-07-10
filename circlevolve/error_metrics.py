import skimage.metrics  # For similarity measurement


def mean_squared_error(image, source):
    return skimage.metrics.mean_squared_error(image, source)


def structural_similarity_error(image, source):
    return -1 * skimage.metrics.structural_similarity(image, source, multichannel=True)
