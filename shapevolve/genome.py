"""The Genome class represents a shape sequence and its various properties, from which an image can be built."""

import pickle

import numpy as np

from utils import unadjust


class MismatchedGenomeError(Exception):
    """An error that occurs when two genomes do not share the same properties with one another."""
    pass


class Genome:
    """This class represents a shape sequence and its various properties, from which an image can be built."""

    def __init__(self, sequence, ratio, height, width, background_color, adjusters, palette, draw):
        """Constructs a genome based on certain properties.

        :param sequence: A sequence of Gene objects that represent the shapes in the image.
        :param ratio: The ratio between the evolution image dimensions and the original image dimensions.
        :param height: The height of the image.
        :param width: The width of the image.
        :param background_color: The background color of the image.
        :param adjusters: Reversible image adjusters that can be applied and unapplied to the image.
        :param palette: A list of RGB color tuples that colors are referenced from.
        :param draw: A function that is used to draw an image according to a Gene object.
        :type sequence: List[Gene]
        :type ratio: float
        :type height: int
        :type width: int
        :type background_color: Tuple[int, int, int]
        :type adjusters: List[Dict[str, Callable]]
        :type palette: List[Tuple[int, int, int]]
        :type draw: Callable
        """
        self.sequence = sequence
        self.ratio = ratio
        self.height = height
        self.width = width
        self.background_color = background_color
        self.adjusters = adjusters
        self.palette = palette
        self.draw = draw

    def render_scaled_image(self, after_unadjustment=False, fill_gaps=True):
        """Renders a scaled version of an image according to the genome's ratio field.

        :param after_unadjustment: Whether the image has already been un-adjusted.
        :param fill_gaps: Whether gaps should be filled in the scaled image.
        :type after_unadjustment: bool
        :type fill_gaps: bool
        :return: The scaled image.
        :rtype: ndarray
        """
        scaled_height = round(self.height / self.ratio)
        scaled_width = round(self.width / self.ratio)
        scaled_sequence = self.scale_sequence(fill_gaps)
        scaled_image = self.render_image(scaled_height, scaled_width, scaled_sequence, after_unadjustment)

        return scaled_image

    def scale_sequence(self, fill_gaps):
        """Generates a gene sequence with each gene scaled by the genome's ratio field.

        :param fill_gaps: Whether the gene's radius should be adjusted to fill new gaps in the scaled image.
        :type fill_gaps: bool
        :return: The new Gene sequence.
        :rtype: List[Gene]
        """
        return [gene.get_scaled_version(self.ratio, fill_gaps) for gene in self.sequence]

    def render_raw_image(self, after_unadjustment=False):
        """Renders the image without any scaling.

        :param after_unadjustment: Whether the image has already been un-adjusted.
        :type after_unadjustment: bool
        :return: The rendered image.
        :rtype: ndarray
        """
        return self.render_image(self.height, self.width, self.sequence, after_unadjustment)

    def render_image(self, height, width, sequence, after_unadjustment):
        """Renders an image according to certain parameters.

        :param height: The height of the desired image.
        :param width: The width of the desired image.
        :param sequence: The gene sequence to draw on the image.
        :param after_unadjustment: Whether the image has already been un-adjusted.
        :type height: int
        :type width: int
        :type sequence: List[Gene]
        :type after_unadjustment: bool
        :return: The rendered image.
        :rtype: ndarray
        """
        image = np.zeros((height, width, 3), np.uint8)
        image[:] = self.background_color

        for gene in sequence:
            self.draw(image, gene, self.palette)
        if after_unadjustment:
            image = unadjust(image, self.adjusters)
        return image

    def save_genome(self, filename):
        """Saves the genome to a file using pickle.

        :param filename: The filename to save the genome to.
        :type filename: str
        """
        with open(filename, 'wb') as genomeFile:
            pickle.dump(self, genomeFile)


def is_compatible(genome1, genome2):
    """Check whether two genomes could describe the same base image.

    :param genome1: Genome 1, to be compared.
    :param genome2: Genome 2, to be compared.
    :type genome1: Genome
    :type genome2: Genome
    :return: Whether they are matched.
    :rtype: bool
    :raises: MismatchedGenomeError: If the genomes do not match.
    """
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


def load_genome(filename):
    """Loads a pickled Genome file.

    :param filename: The filename of the genome to be loaded.
    :type filename: str
    :return: The loaded genome.
    :rtype: Genome
    """
    with open(filename, 'rb') as genomeFile:
        genome = pickle.load(genomeFile)
    return genome
