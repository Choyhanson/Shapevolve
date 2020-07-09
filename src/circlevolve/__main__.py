from matplotlib.pyplot import show

from adjusters import DARK_ADJUSTER
from drawers import add_square
from evolver import Evolver
from genome import Genome
from preprocessors import contrast_preprocess, saturate_preprocess, smooth_preprocess
from utils import get_image_path

IMAGE_DIRECTORY = "sample-images"
MONALISA = get_image_path("monalisa.jpg", IMAGE_DIRECTORY)
PEARLEARRING = get_image_path("pearlearring.jpg", IMAGE_DIRECTORY)
STARRYNIGHT = get_image_path("starrynight.png", IMAGE_DIRECTORY)


def dark_sample(path):
    evolver = Evolver(path, adjusters=[DARK_ADJUSTER])
    evolver.evolve(num_generations=1000)


def regular_sample(path):
    evolver = Evolver(path)
    evolver.evolve()


def saturation_sample(path):
    evolver = Evolver(path, preprocesses=[saturate_preprocess, contrast_preprocess, smooth_preprocess])
    evolver.evolve(num_generations=1000)


def square_sample(path):
    evolver = Evolver(path, draw=add_square)
    evolver.evolve(num_generations=1000)


def save_sample(path):
    evolver = Evolver(path)
    genome = evolver.evolve(num_generations=300)
    genome.save_genome(path + "_genome.pkl")


def load_sample(path):
    saved_genome = Genome.load_genome(path + "_genome.pkl")
    evolver = Evolver(path, saved_genome=saved_genome)
    evolver.evolve(num_generations=300)


if __name__ == '__main__':
    regular_sample(STARRYNIGHT)
    show()
