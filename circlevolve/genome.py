import pickle

import numpy as np

from utils import unadjust


class MismatchedGenomeError(Exception):
    pass


class Genome:  # Represents an entire image's circle sequence and properties.
    def __init__(self, sequence, ratio, height, width, background_color, adjusters, palette, draw):  # basic constructor
        self.sequence = sequence
        self.ratio = ratio
        self.height = height
        self.width = width
        self.background_color = background_color
        self.adjusters = adjusters
        self.palette = palette
        self.draw = draw

    def render_scaled_image(self, after_unadjustment=True, fill_gaps=True):  # render the image, scaled to its ratio.
        scaled_height = round(self.height / self.ratio)
        scaled_width = round(self.width / self.ratio)
        scaled_sequence = self.scale_sequence(fill_gaps)
        scaled_image = self.render_image(scaled_height, scaled_width, scaled_sequence, after_unadjustment)

        return scaled_image

    def scale_sequence(self, fill_gaps):  # scale each circle in the gene sequence by the ratio.
        return [gene.get_scaled_version(self.ratio, fill_gaps) for gene in self.sequence]

    def render_raw_image(self, after_unadjustment=True):  # render the image without scaling.
        return self.render_image(self.height, self.width, self.sequence, after_unadjustment)

    def render_image(self, height, width, sequence, after_unadjustment):  # renders the image according to parameters.
        image = np.zeros((height, width, 3), np.uint8)
        image[:] = self.background_color

        for gene in sequence:
            self.draw(image, gene, self.palette)
        if after_unadjustment:
            image = unadjust(image, self.adjusters)
        return image

    def save_genome(self, filename):  # Saves the genome to a pickle file.
        with open(filename, 'wb') as genomeFile:
            pickle.dump(self, genomeFile)

    @staticmethod
    def load_genome(filename):  # Loads a genome from a pickle file.
        with open(filename, 'rb') as genomeFile:
            genome = pickle.load(genomeFile)
        return genome

    @staticmethod
    def isCompatible(genome1, genome2):
        gene_checks = ['max_radius', 'min_radius', 'height', 'width', 'num_colors']
        genome_checks = ['ratio', 'height', 'width', 'background_color', 'adjusters', 'palette', 'draw']

        for gene1, gene2 in zip(genome1.sequence, genome2.sequence):
            gene1_dict = vars(gene1)
            gene2_dict = vars(gene2)
            for check in gene_checks:
                if gene1_dict[check] != gene2_dict[check]:
                    raise MismatchedGenomeError(f"Genome match was inconsistent: {check} field was incorrect. "
                                                f"Please make sure the source image matches the genome you are "
                                                f"trying to load.")

        if len(genome1.sequence) != len(genome2.sequence):
            raise MismatchedGenomeError(f"Genome match was inconsistent: gene sequences had different lengths. "
                                        f"Please make sure the source image matches the genome you are "
                                        f"trying to load.")

        genome1dict = vars(genome1)
        genome2dict = vars(genome2)
        for check in genome_checks:
            if genome1dict[check] != genome2dict[check]:
                raise MismatchedGenomeError(f"Genome match was inconsistent: {check} field was incorrect. "
                                            f"Please make sure the source image matches the genome you are "
                                            f"trying to load.")

        return True
