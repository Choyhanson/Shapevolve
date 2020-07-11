"""Some sample methods to show the functionality of the module."""

import cv2

# noinspection PyUnresolvedReferences
from shapevolve import callbacks
from shapevolve.adjusters import STRONG_DARK_ADJUSTER
from shapevolve.drawers import add_square
from shapevolve.error_metrics import structural_similarity_error
from shapevolve.evolver import Evolver
from shapevolve.genome import load_genome
from shapevolve.preprocessors import contrast_preprocess, saturate_preprocess, smooth_preprocess
from shapevolve.utils import get_image_path, get_image

IMAGE_DIRECTORY = "samples"
MONALISA = get_image_path("monalisa.jpg", IMAGE_DIRECTORY)
PEARLEARRING = get_image_path("pearlearring.jpg", IMAGE_DIRECTORY)
STARRYNIGHT = get_image_path("starrynight.png", IMAGE_DIRECTORY)
GREATWAVE = get_image_path("greatwave.jpg", IMAGE_DIRECTORY)


def standard_sample(filepath):
    """A standard sample function that illustrates how to use the module.

    :param filepath: The absolute filepath of an input image.
    :type filepath: str
    :return: The evolved genome.
    :rtype: Genome
    """
    evolver = Evolver(get_image(filepath))
    return evolver.evolve()


def adjustment_sample(filepath):
    """A sample function that illustrates how to use adjusters.

    :param filepath: The absolute filepath of an input image.
    :type filepath: str
    :return: The evolved genome.
    :rtype: Genome
    """
    evolver = Evolver(get_image(filepath), adjusters=[STRONG_DARK_ADJUSTER])
    return evolver.evolve()


def preprocess_sample(filepath):
    """A sample function that illustrates how to use preprocesses.

    :param filepath: The absolute filepath of an input image.
    :type filepath: str
    :return: The evolved genome.
    :rtype: Genome
    """
    evolver = Evolver(get_image(filepath), preprocesses=[saturate_preprocess, contrast_preprocess, smooth_preprocess])
    return evolver.evolve()


def error_metric_sample(filepath):
    """A sample function that illustrates how to use custom error metrics.

    :param filepath: The absolute filepath of an input image.
    :type filepath: str
    :return: The evolved genome.
    :rtype: Genome
    """
    evolver = Evolver(get_image(filepath), calculate_error=structural_similarity_error)
    return evolver.evolve()


def draw_shape_sample(filepath):
    """A sample function that illustrates how to use custom shape drawing methods.

    :param filepath: The absolute filepath of an input image.
    :type filepath: str
    :return: The evolved genome.
    :rtype: Genome
    """
    evolver = Evolver(get_image(filepath), draw=add_square)
    return evolver.evolve()


def save_genome_sample(filepath_source, filepath_to_save_to):
    """A sample function that illustrates how to save genomes.

    :param filepath_source: The absolute filepath of an input image.
    :type filepath_source: str
    :param filepath_to_save_to: The filepath to save the genome.
    :type filepath_to_save_to: str
    :return: The evolved genome.
    :rtype: Genome
    """
    evolver = Evolver(get_image(filepath_source))
    genome = evolver.evolve()
    genome.save_genome(filepath_to_save_to)
    return genome


def load_genome_sample(filepath_source, filepath_genome):
    """A sample function that illustrates how to load previously saved genomes.

    :param filepath_source: The absolute filepath of an input image.
    :type filepath_source: str
    :param filepath_genome: The filepath to load the pre-evolved genome.
    :type filepath_genome: str
    :return: The evolved genome.
    :rtype: Genome
    """
    evolver = Evolver(get_image(filepath_source), saved_genome=load_genome(filepath_genome))
    return evolver.evolve()


def save_image_sample(filepath_source, filepath_to_save_to):
    """A sample function that illustrates how to save images from genomes.

    :param filepath_source: The absolute filepath of an input image.
    :type filepath_source: str
    :param filepath_to_save_to: The filepath to save the evolved image to.
    :type filepath_to_save_to: str
    :return: The evolved genome.
    :rtype: Genome
    """
    evolver = Evolver(get_image(filepath_source))
    genome = evolver.evolve()
    image = genome.render_scaled_image()
    cv2.imwrite(filepath_to_save_to, image)
    return genome


def callback_sample(filepath_source, filepath_csv):
    """A sample function that illustrates how to add callbacks to the evolve method.

    :param filepath_source: The absolute filepath of an input image.
    :type filepath_source: str
    :param filepath_csv: The filepath to save CSV statistics to.
    :type filepath_csv: str
    :return: The evolved genome.
    :rtype: Genome
    """
    evolver = Evolver(get_image(filepath_source))
    logger = callbacks.CSVLogger(filepath_csv)
    return evolver.evolve(callbacks=[callbacks.default_callback, logger.callback])
