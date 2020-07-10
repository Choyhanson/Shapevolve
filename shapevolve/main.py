"""The main CLI interface for the standalone app."""

from argparse import ArgumentParser

from cv2 import imwrite
from matplotlib.pyplot import show

from evolver import Evolver
from genome import load_genome
from utils import get_image


def main():
    """Run the application."""
    parser = ArgumentParser(description="Circlevolve CLI")
    parser.add_argument("image", type=str, help="Path to base image for evolution")
    parser.add_argument("--saved-genome", default=None, type=str, help="Path to saved genome for continued evolution")
    parser.add_argument("--num-shapes", default=1000, type=int, help="Number of shapes to draw with")
    parser.add_argument("--num-generations", default=5000, type=int, help="Number of generations to train")
    args = parser.parse_args()

    if args.saved_genome is not None:
        saved_genome = load_genome(args.saved_genome)
    else:
        saved_genome = None

    image_path = args.image + "_result.png"
    genome_path = args.image + "_genome.pkl"

    evolver = Evolver(get_image(args.image), saved_genome=saved_genome, num_shapes=args.num_shapes)
    genome = evolver.evolve(num_generations=args.num_generations)
    image = genome.render_scaled_image()

    imwrite(image_path, image)
    genome.save_genome(genome_path)
    print(f"Image saved at {image_path}\nGenome saved at {genome_path}")

    show()  # Keep matplotlib window open.
