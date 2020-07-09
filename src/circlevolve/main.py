from argparse import ArgumentParser

from cv2 import imwrite
from matplotlib.pyplot import show

from evolver import Evolver
from utils import get_image


def main():
    parser = ArgumentParser(description="Circlevolve CLI")
    parser.add_argument("image", type=str, help="Path to base image for evolution")
    parser.add_argument("--num-shapes", default=1000, type=int, help="Number of shapes to draw with")
    parser.add_argument("--num-generations", default=5000, type=int, help="Number of generations to train")
    args = parser.parse_args()

    evolver = Evolver(get_image(args.image), num_shapes=args.num_shapes)
    genome = evolver.evolve(num_generations=args.num_generations)
    image = genome.render_scaled_image()
    imwrite(args.source_image_path + "_result.png", image)
    genome.save_genome(args.source_image_path + "_genome.pkl")
    show()
