import pickle

import numpy as np

from utils import add_circle


class Genome:  # Represents an entire image's circle sequence and properties.
    def __init__(self, sequence, ratio, height, width, background_color, adjuster, palette):  # basic constructor
        self.sequence = sequence
        self.ratio = ratio
        self.height = height
        self.width = width
        self.background_color = background_color
        self.adjuster = adjuster
        self.palette = palette

    def render_scaled_image(self):  # render the image, scaled to its ratio.
        scaled_height = int(self.height / self.ratio)
        scaled_width = int(self.width / self.ratio)
        scaled_sequence = self.scale_sequence()
        scaled_image = self.render_image(scaled_height, scaled_width, scaled_sequence)

        return scaled_image

    def scale_sequence(self):  # scale each circle in the gene sequence by the ratio.
        return [gene.get_scaled_version(self.ratio) for gene in self.sequence]

    def render_raw_image(self):  # render the image without scaling.
        return self.render_image(self.height, self.width, self.sequence)

    def render_image(self, height, width, sequence):  # renders the image according to parameters.
        image = np.zeros((height, width, 3), np.uint8)
        image[:] = self.background_color

        for gene in sequence:
            add_circle(image, gene, self.palette)
        return image

    def save_genome(self, filename):  # Saves the genome to a pickle file.
        with open(filename, 'wb') as genomeFile:
            pickle.dump(self, genomeFile)

    @staticmethod
    def load_genome(filename):  # Loads a genome from a pickle file.
        with open(filename, 'rb') as genomeFile:
            genome = pickle.load(genomeFile)
        return genome
