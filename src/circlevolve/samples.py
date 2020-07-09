import cv2

import callbacks
from adjusters import STRONG_DARK_ADJUSTER
from drawers import add_square
from error_metrics import structural_similarity_error
from evolver import Evolver
from genome import Genome
from preprocessors import contrast_preprocess, saturate_preprocess, smooth_preprocess
from utils import get_image_path, get_image

IMAGE_DIRECTORY = "sample-images"
MONALISA = get_image_path("monalisa.jpg", IMAGE_DIRECTORY)
PEARLEARRING = get_image_path("pearlearring.jpg", IMAGE_DIRECTORY)
STARRYNIGHT = get_image_path("starrynight.png", IMAGE_DIRECTORY)
GREATWAVE = get_image_path("greatwave.jpg", IMAGE_DIRECTORY)


def standard_sample(filepath):
    evolver = Evolver(get_image(filepath))
    return evolver.evolve()


def adjustment_sample(filepath):
    evolver = Evolver(get_image(filepath), adjusters=[STRONG_DARK_ADJUSTER])
    return evolver.evolve()


def preprocess_sample(filepath):
    evolver = Evolver(get_image(filepath), preprocesses=[saturate_preprocess, contrast_preprocess, smooth_preprocess])
    return evolver.evolve()


def error_metric_sample(filepath):
    evolver = Evolver(get_image(filepath), calculate_error=structural_similarity_error)
    return evolver.evolve()


def draw_shape_sample(filepath):
    evolver = Evolver(get_image(filepath), draw=add_square)
    return evolver.evolve()


def save_genome_sample(filepath_source, filepath_to_save_to):
    evolver = Evolver(get_image(filepath_source))
    genome = evolver.evolve()
    genome.save_genome(filepath_to_save_to)
    return genome


def load_genome_sample(filepath_source, filepath_genome):
    evolver = Evolver(get_image(filepath_source), saved_genome=Genome.load_genome(filepath_genome))
    return evolver.evolve()


def save_image_sample(filepath_source, filepath_to_save_to):
    evolver = Evolver(get_image(filepath_source))
    genome = evolver.evolve()
    image = genome.render_scaled_image()
    cv2.imwrite(filepath_to_save_to, image)
    return genome


def callback_sample(filepath_source, filepath_csv):
    evolver = Evolver(get_image(filepath_source))
    logger = callbacks.CSVLogger(filepath_csv)
    return evolver.evolve(callbacks=[callbacks.default_callback, logger.callback])
