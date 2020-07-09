from matplotlib.pyplot import show

import callbacks
from adjusters import STRONG_DARK_ADJUSTER
from drawers import add_square
from evolver import Evolver
from genome import Genome
from preprocessors import contrast_preprocess, saturate_preprocess, smooth_preprocess
from utils import get_image_path

IMAGE_DIRECTORY = "sample-images"
MONALISA = get_image_path("monalisa.jpg", IMAGE_DIRECTORY)
PEARLEARRING = get_image_path("pearlearring.jpg", IMAGE_DIRECTORY)
STARRYNIGHT = get_image_path("starrynight.png", IMAGE_DIRECTORY)
GREATWAVE = get_image_path("greatwave.jpg", IMAGE_DIRECTORY)


def dark_sample(path):
    evolver = Evolver(path, adjusters=[STRONG_DARK_ADJUSTER])
    return evolver.evolve(num_generations=1000)


def regular_sample(path):
    evolver = Evolver(path)
    return evolver.evolve(num_generations=4000)


def saturation_sample(path):
    evolver = Evolver(path, preprocesses=[saturate_preprocess, contrast_preprocess, smooth_preprocess])
    return evolver.evolve(num_generations=1000)


def square_sample(path):
    evolver = Evolver(path, draw=add_square)
    return evolver.evolve(num_generations=1000)


def save_sample(path):
    evolver = Evolver(path)
    genome = evolver.evolve()
    genome.save_genome(path + "_genome.pkl")
    return genome


def load_sample(path):
    saved_genome = Genome.load_genome(path + "_genome.pkl")
    evolver = Evolver(path, saved_genome=saved_genome)
    return evolver.evolve(num_generations=300)


def save_image_sample(path):
    evolver = Evolver(path)
    image_saver = callbacks.QuietHighQualityImageSaver(get_image_path("trial", IMAGE_DIRECTORY))
    return evolver.evolve(num_generations=200, callbacks=[callbacks.default_callback, image_saver.callback])


def save_csv_sample(path):
    evolver = Evolver(path)
    logger = callbacks.CSVLogger(get_image_path("trial.csv", IMAGE_DIRECTORY))
    return evolver.evolve(num_generations=200, callbacks=[callbacks.default_callback, logger.callback])


if __name__ == '__main__':
    save_sample(GREATWAVE)
    show()
