"""The main CLI interface for the standalone app."""

from argparse import ArgumentParser

from cv2 import imwrite
from matplotlib.pyplot import show

from shapevolve.evolver import Evolver
from shapevolve.genome import load_genome
from shapevolve.utils import get_image
from shapevolve import __version__, callbacks, drawers, error_metrics, adjusters


def main():
    """Run the application."""
    parser = ArgumentParser(description=f"Circlevolve CLI, version {__version__}")
    parser.add_argument("image", type=str, help="Path to base image for evolution")
    parser.add_argument("-square",  dest="square", action='store_true', help="Runs with squares instead of circles")
    parser.add_argument("-debug", dest="debug", action='store_true', help="Print statistics in console")
    parser.add_argument("-ssim", dest="ssim", action='store_true', help="Use structural-similarity instead of mean-squared-error")
    parser.add_argument("-dark", dest="dark", action='store_true', help="Optimize the algorithm for darker images")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-silent", dest="output", action='store_const', const=2, help="Disables viewing updates and statistics during evolution")
    group.add_argument("-quiet", dest="output", action='store_const', const=1, help="Updates more rarely during evolution")

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

    if args.square:
        draw = drawers.add_square
    else:
        draw = drawers.add_circle

    if args.ssim:
        error = error_metrics.structural_similarity_error
    else:
        error = error_metrics.mean_squared_error

    if args.dark:
        adjustments = [adjusters.STRONG_DARK_ADJUSTER]
    else:
        adjustments = []

    if args.output == 2:
        silent = True
    else:
        silent = False

    if args.output == 1:
        callback_list = [callbacks.quiet_visual_callback]
        if args.debug:
            callback_list.append(callbacks.quiet_verbose_callback)
    else:
        callback_list = [callbacks.visual_callback]
        if args.debug:
            callback_list.append(callbacks.verbose_callback)

    evolver = Evolver(get_image(args.image), saved_genome=saved_genome, num_shapes=args.num_shapes, draw=draw, calculate_error=error, adjusters=adjustments)
    print("evolve!")
    genome = evolver.evolve(num_generations=args.num_generations, silent=silent, callbacks=callback_list)
    image = genome.render_scaled_image()

    imwrite(image_path, image)
    genome.save_genome(genome_path)
    print(f"Image saved at {image_path}\nGenome saved at {genome_path}")

    show()  # Keep matplotlib window open.
