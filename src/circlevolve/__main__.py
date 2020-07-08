from evolver import Evolver
from utils import get_image_path

IMAGE_DIRECTORY = "sample-images"
MONALISA = get_image_path("monalisa.jpg", IMAGE_DIRECTORY)
PEARLEARRING = get_image_path("pearlearring.jpg", IMAGE_DIRECTORY)
STARRYNIGHT = get_image_path("starrynight.png", IMAGE_DIRECTORY)

if __name__ == '__main__':
    evolver = Evolver(STARRYNIGHT)
    evolver.evolve(num_generations=2000)
