"""A Gene class that defines the properties of a single shape on an image."""

from random import random, randint


class Gene:
    """A Gene class that defines the properties of a single shape on an image."""

    def __init__(self, max_radius, min_radius, height, width, num_colors, radius=None, center=None, color=None,
                 alpha=None):
        """Constructs a gene and its initial properties.

        :param max_radius: The maximum possible radius the gene can have.
        :param min_radius: The minimum possible radius the gene can have.
        :param height: The height of the image that the gene is drawing on.
        :param width: The width of the image that the gene is drawing on.
        :param num_colors: The number of colours the gene can have.
        :param radius: The current radius of the gene.
        :param center: The coordinates of the center of the gene's shape.
        :param color: The current color of the gene, as an index of an external color palette list.
        :param alpha: The current opacity of the gene, between 0 and 1.
        :type max_radius: int
        :type min_radius: int
        :type height: int
        :type width: int
        :type num_colors: int
        :type radius: int
        :type center: Tuple[int, int]
        :type color: int
        :type alpha: float
        """
        self.max_radius = max_radius
        self.min_radius = min_radius
        self.height = height
        self.width = width
        self.num_colors = num_colors
        if radius is None:
            self.completely_randomize(initialization=True)  # Randomize values at initialization.
        else:
            self.radius = radius
            self.center = center
            self.color = color
            self.alpha = alpha
            self.history = [radius, center, color, alpha]

    def revert(self):
        """Reverts the gene's properties to before it was last modified."""
        self.radius = self.history[0]
        self.center = self.history[1]
        self.color = self.history[2]
        self.alpha = self.history[3]

    def completely_randomize(self, initialization=False):
        """Completely randomizes the properties of the gene.

        :param initialization: Whether this is being called from the constructor.
        :type initialization: bool
        """
        self.randomize_radius()
        self.randomize_center()
        self.randomize_color()
        self.randomize_alpha()
        if initialization:
            self.history = [self.radius, self.center, self.color, self.alpha]

    def mutate(self):
        """Mutates the gene randomly."""

        # backup
        self.history = [self.radius, self.center, self.color, self.alpha]

        # Chances of altering the radius or alpha
        radius_alter = random() < 0.293
        alpha_alter = random() < 0.293

        # Whether an alteration still needs to be made
        no_alter = not (radius_alter or alpha_alter)

        # Mutate.
        if radius_alter:
            self.randomize_radius()
        if alpha_alter:
            self.randomize_alpha()
        if no_alter:
            self.completely_randomize()

    def randomize_radius(self):
        """Randomizes the radius."""
        self.radius = randint(self.min_radius, self.max_radius)

    def randomize_center(self):
        """Randomizes the center of the shape."""

        # The center can be a little bit outside the width and height of the image.
        self.center = (randint(0 - round(self.radius / 5), self.width + round(self.radius / 5)),
                       randint(0 - round(self.radius / 5), self.height + round(self.radius / 5)))

    def randomize_color(self):
        """Randomizes the color of the shape."""
        self.color = randint(0, self.num_colors - 2)  # The num_colors is off by one because of ColorThief.

    def randomize_alpha(self):
        """Randomizes the opacity of the shape."""
        self.alpha = random() * 0.45 + 0.05  # between 0.05 and 0.5

    def get_scaled_version(self, ratio, fill_gaps):
        """Creates a scaled version of the gene, according to some ratio (original dimension / scaled dimension)

        :param ratio: (original dimension) / (scaled dimension)
        :param fill_gaps: Whether the radii should be slightly expanded so gaps don't form between shapes.
        :return: The scaled gene.
        :rtype: Gene
        """
        radius_padding = 1 if fill_gaps else 0
        new_radius = round((self.radius + radius_padding) / ratio)
        new_center = (round(self.center[0] / ratio), round(self.center[1] / ratio))
        new_height = round(self.height / ratio)
        new_width = round(self.width / ratio)
        new_max_radius = round(self.max_radius / ratio)
        new_min_radius = round(self.min_radius / ratio)
        return Gene(new_max_radius, new_min_radius, new_height, new_width, self.num_colors, new_radius, new_center,
                    self.color, self.alpha)

    def clone(self):
        """Clones itself."""
        return Gene(self.max_radius, self.min_radius, self.height, self.width, self.num_colors, self.radius,
                    self.center, self.color, self.alpha)
