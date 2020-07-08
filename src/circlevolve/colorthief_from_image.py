from colorthief import ColorThief


class ColorThiefFromImage(ColorThief):  # Extend ColorThief to support providing images as-is instead of filenames
    # noinspection PyMissingConstructor
    def __init__(self, image):
        self.image = image
