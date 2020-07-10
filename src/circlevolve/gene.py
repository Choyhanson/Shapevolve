from random import random, randint


class Gene:  # Defines a single gene, which describes how to draw a single circle.
    def __init__(self, max_radius, min_radius, height, width, num_colors, radius=None, center=None, color=None,
                 alpha=None):  # Basic constructor.  Leave default parameters empty for randomization.
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

    def revert(self):  # Reverts circle to previous properties (in case a mutation was unhelpful.)
        self.radius = self.history[0]
        self.center = self.history[1]
        self.color = self.history[2]
        self.alpha = self.history[3]

    def completely_randomize(self, initialization=False):  # Completely randomizes the values
        self.randomize_radius()
        self.randomize_center()
        self.randomize_color()
        self.randomize_alpha()
        if initialization:
            self.history = [self.radius, self.center, self.color, self.alpha]

    def mutate(self):  # Mutates a circle randomly.  If complete is True, this will always perform a complete mutation.
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

    def randomize_radius(self):  # randomizes radius
        self.radius = randint(self.min_radius, self.max_radius)

    def randomize_center(self):  # randomizes center of circle
        self.center = (randint(0 - round(self.radius / 5), self.width + round(self.radius / 5)),
                       randint(0 - round(self.radius / 5), self.height + round(self.radius / 5)))

    def randomize_color(self):  # randomizes color
        self.color = randint(0, self.num_colors - 2)

    def randomize_alpha(self):  # randomizes alpha
        self.alpha = random() * 0.45 + 0.05

    def get_scaled_version(self, ratio):  # Creates a new gene that represents the circle scaled by some ratio.
        new_radius = round((self.radius + 1) / ratio)
        new_center = (round(self.center[0] / ratio), round(self.center[1] / ratio))
        new_height = round(self.height / ratio)
        new_width = round(self.width / ratio)
        new_max_radius = round(self.max_radius / ratio)
        new_min_radius = round(self.min_radius / ratio)
        return Gene(new_max_radius, new_min_radius, new_height, new_width, self.num_colors, new_radius, new_center,
                    self.color, self.alpha)

    def clone(self):  # Creates a copy of itself.
        return Gene(self.max_radius, self.min_radius, self.height, self.width, self.num_colors, self.radius,
                    self.center, self.color, self.alpha)
