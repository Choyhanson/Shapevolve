"""Callbacks that can be given to the Evolver class, to be run when a successful change is applied to the genome."""

import csv

from matplotlib.pyplot import savefig

import cv2

from shapevolve.utils import show_image

_display = None


def default_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                     complex_mutation, best_image, genome):
    """The default callback that the Evolver class uses. Currently visual_callback.

    :param offspring: The total number of offspring already processed.
    :param changes: The total number of changes already applied to the genome.
    :param loop_index: The total number of loops already performed.
    :param num_mutation_type_switches: The total number of switches between simple and complex mutations so far.
    :param error: The error of the current genome compared to the base image.
    :param complex_mutation: Whether complex mutations are being applied or not.
    :param best_image: The best image so far.
    :param genome: The genome for the best image so far.
    :type offspring: int
    :type changes: int
    :type loop_index: int
    :type num_mutation_type_switches: int
    :type error: float
    :type complex_mutation: bool
    :type best_image: ndarray
    :type genome: Genome
    """
    visual_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                    complex_mutation, best_image, genome)


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
def visual_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                    complex_mutation, best_image, genome):
    """A simple callback that uses matplotlib to provide a live update of the image on the screen.

    :param offspring: The total number of offspring already processed.
    :param changes: The total number of changes already applied to the genome.
    :param loop_index: The total number of loops already performed.
    :param num_mutation_type_switches: The total number of switches between simple and complex mutations so far.
    :param error: The error of the current genome compared to the base image.
    :param complex_mutation: Whether complex mutations are being applied or not.
    :param best_image: The best image so far.
    :param genome: The genome for the best image so far.
    :type offspring: int
    :type changes: int
    :type loop_index: int
    :type num_mutation_type_switches: int
    :type error: float
    :type complex_mutation: bool
    :type best_image: ndarray
    :type genome: Genome
    """
    _visualize(best_image, genome.adjusters, changes)


def quiet_visual_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                          complex_mutation, best_image, genome):
    """The same thing as visual_callback, but this only runs every 50 generations.

    :param offspring: The total number of offspring already processed.
    :param changes: The total number of changes already applied to the genome.
    :param loop_index: The total number of loops already performed.
    :param num_mutation_type_switches: The total number of switches between simple and complex mutations so far.
    :param error: The error of the current genome compared to the base image.
    :param complex_mutation: Whether complex mutations are being applied or not.
    :param best_image: The best image so far.
    :param genome: The genome for the best image so far.
    :type offspring: int
    :type changes: int
    :type loop_index: int
    :type num_mutation_type_switches: int
    :type error: float
    :type complex_mutation: bool
    :type best_image: ndarray
    :type genome: Genome
    """
    if changes % 50 == 0:
        visual_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                        complex_mutation, best_image, genome)


# noinspection PyUnusedLocal,PyUnusedLocal
def verbose_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                     complex_mutation, best_image, genome):
    """A callback that prints the status of the evolution into standard output.

    :param offspring: The total number of offspring already processed.
    :param changes: The total number of changes already applied to the genome.
    :param loop_index: The total number of loops already performed.
    :param num_mutation_type_switches: The total number of switches between simple and complex mutations so far.
    :param error: The error of the current genome compared to the base image.
    :param complex_mutation: Whether complex mutations are being applied or not.
    :param best_image: The best image so far.
    :param genome: The genome for the best image so far.
    :type offspring: int
    :type changes: int
    :type loop_index: int
    :type num_mutation_type_switches: int
    :type error: float
    :type complex_mutation: bool
    :type best_image: ndarray
    :type genome: Genome
    """
    print(f"Total offspring: {offspring}")
    print(f"Total changes: {changes}")
    print(f"Total loop iterations: {loop_index}")
    print(f"Total mutation type switches: {num_mutation_type_switches}")
    print(f"Current error: {error}")
    extreme = "Yes" if complex_mutation else "No"
    print(f"Is currently in a complex mutation: {extreme}")


def quiet_verbose_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                           complex_mutation, best_image, genome):
    """The same thing as verbose_callback, but this only runs every 50 generations.

    :param offspring: The total number of offspring already processed.
    :param changes: The total number of changes already applied to the genome.
    :param loop_index: The total number of loops already performed.
    :param num_mutation_type_switches: The total number of switches between simple and complex mutations so far.
    :param error: The error of the current genome compared to the base image.
    :param complex_mutation: Whether complex mutations are being applied or not.
    :param best_image: The best image so far.
    :param genome: The genome for the best image so far.
    :type offspring: int
    :type changes: int
    :type loop_index: int
    :type num_mutation_type_switches: int
    :type error: float
    :type complex_mutation: bool
    :type best_image: ndarray
    :type genome: Genome
    """
    if changes % 50 == 0:
        verbose_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                         complex_mutation, best_image, genome)


def _visualize(best_image, adjusters, changes):
    """Displays an updated image in a matplotlib window.

    :param best_image: The image to be displayed.
    :param adjusters: Adjusters to be reversed for the image.
    :param changes: The current generation number.
    :type best_image: ndarray
    :type adjusters: List[Dict[str, Callable]]
    :type changes: int
    """
    global _display
    if _display is None:
        _display = show_image(best_image, changes, adjusters=adjusters)
    else:
        show_image(best_image, changes, display=_display, adjusters=adjusters)


class GenomeSaver:
    """A class that defines a callback where genomes are saved to files."""

    def __init__(self, genome_root, frequency=1):
        """Constructs a genome saver class that takes a given root file path.

        :param genome_root: The file path where genomes should be saved.
        :param frequency: The frequency at which files will be saved.
        :type genome_root: str
        :type frequency: int
        """
        self.root = genome_root
        self.frequency = frequency

    # noinspection PyUnusedLocal
    def callback(self, offspring, changes, loop_index, num_mutation_type_switches, error,
                 complex_mutation, best_image, genome):
        """A callback that saves genomes to a filepath.

        :param offspring: The total number of offspring already processed.
        :param changes: The total number of changes already applied to the genome.
        :param loop_index: The total number of loops already performed.
        :param num_mutation_type_switches: The total number of switches between simple and complex mutations so far.
        :param error: The error of the current genome compared to the base image.
        :param complex_mutation: Whether complex mutations are being applied or not.
        :param best_image: The best image so far.
        :param genome: The genome for the best image so far.
        :type offspring: int
        :type changes: int
        :type loop_index: int
        :type num_mutation_type_switches: int
        :type error: float
        :type complex_mutation: bool
        :type best_image: ndarray
        :type genome: Genome
        """
        if changes % self.frequency == 0:
            genome.save_genome(self.root + f"_gen{changes:04d}.genome")


class CSVLogger:
    """A class that defines callbacks which record statistics into a CSV file."""

    def __init__(self, csv_filepath, frequency=1):
        """A constructor for the class that stores a path to a CSV file.

        :param csv_filepath: The filepath of the CSV file that statistics will be written to.
        :param frequency: The frequency at which stats will be saved.
        :type csv_filepath: str
        :type frequency: int
        """
        self.csv_filepath = csv_filepath
        self.frequency = frequency
        with open(csv_filepath, 'w', newline='') as file:  # Write the headers for the CSV file.
            writer = csv.writer(file)
            writer.writerow(["offspring", "generation", "loop_index", "error"])

    # noinspection PyUnusedLocal
    def callback(self, offspring, changes, loop_index, num_mutation_type_switches, error,
                 complex_mutation, best_image, genome):
        """A callback that stores offspring, generation, loop index, and error into the class's CSV file.

        :param offspring: The total number of offspring already processed.
        :param changes: The total number of changes already applied to the genome.
        :param loop_index: The total number of loops already performed.
        :param num_mutation_type_switches: The total number of switches between simple and complex mutations so far.
        :param error: The error of the current genome compared to the base image.
        :param complex_mutation: Whether complex mutations are being applied or not.
        :param best_image: The best image so far.
        :param genome: The genome for the best image so far.
        :type offspring: int
        :type changes: int
        :type loop_index: int
        :type num_mutation_type_switches: int
        :type error: float
        :type complex_mutation: bool
        :type best_image: ndarray
        :type genome: Genome
        """
        if changes % self.frequency == 0:
            with open(self.csv_filepath, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([offspring, changes, loop_index, error])


class ImageSaver:
    """A class that defines a callback where images built during evolution are saved."""

    def __init__(self, image_root, frequency=1):
        """A constructor for the class that defines a root filepath for saved images.

        :param image_root: The root filepath for saved images.
        :param frequency: The frequency at which files will be saved.
        :type image_root: str
        :type frequency: int
        """
        self.root = image_root
        self.frequency = frequency

    def callback(self, offspring, changes, loop_index, num_mutation_type_switches, error,
                 complex_mutation, best_image, genome):
        """A callback that saves the best image so far into a png file.

        :param offspring: The total number of offspring already processed.
        :param changes: The total number of changes already applied to the genome.
        :param loop_index: The total number of loops already performed.
        :param num_mutation_type_switches: The total number of switches between simple and complex mutations so far.
        :param error: The error of the current genome compared to the base image.
        :param complex_mutation: Whether complex mutations are being applied or not.
        :param best_image: The best image so far.
        :param genome: The genome for the best image so far.
        :type offspring: int
        :type changes: int
        :type loop_index: int
        :type num_mutation_type_switches: int
        :type error: float
        :type complex_mutation: bool
        :type best_image: ndarray
        :type genome: Genome
        """
        if changes % self.frequency == 0:
            if not cv2.imwrite(self.root + f"_img{changes:04d}.png", best_image):
                raise FileNotFoundError("The path given to ImageSaver was not valid.")


class HighQualityImageSaver(ImageSaver):
    """A subclass of ImageSaver that scales images to the original resolution before saving them."""

    def callback(self, offspring, changes, loop_index, num_mutation_type_switches, error,
                 complex_mutation, best_image, genome):
        """A callback that scales an image before providing it to the equivalent method in ImageSaver.

        :param offspring: The total number of offspring already processed.
        :param changes: The total number of changes already applied to the genome.
        :param loop_index: The total number of loops already performed.
        :param num_mutation_type_switches: The total number of switches between simple and complex mutations so far.
        :param error: The error of the current genome compared to the base image.
        :param complex_mutation: Whether complex mutations are being applied or not.
        :param best_image: The best image so far.
        :param genome: The genome for the best image so far.
        :type offspring: int
        :type changes: int
        :type loop_index: int
        :type num_mutation_type_switches: int
        :type error: float
        :type complex_mutation: bool
        :type best_image: ndarray
        :type genome: Genome
        """
        image = genome.render_scaled_image()
        ImageSaver.callback(self, offspring, changes, loop_index, num_mutation_type_switches, error,
                            complex_mutation, image, genome)


class MatplotImageSaver(ImageSaver):
    """A class that defines a callback where images shown by matplotlib during evolution are saved. Must be used with a variant of visual_callback in the same list."""

    def callback(self, offspring, changes, loop_index, num_mutation_type_switches, error,
                 complex_mutation, best_image, genome):
        """A callback that saves the best image so far into a png file.

        :param offspring: The total number of offspring already processed.
        :param changes: The total number of changes already applied to the genome.
        :param loop_index: The total number of loops already performed.
        :param num_mutation_type_switches: The total number of switches between simple and complex mutations so far.
        :param error: The error of the current genome compared to the base image.
        :param complex_mutation: Whether complex mutations are being applied or not.
        :param best_image: The best image so far.
        :param genome: The genome for the best image so far.
        :type offspring: int
        :type changes: int
        :type loop_index: int
        :type num_mutation_type_switches: int
        :type error: float
        :type complex_mutation: bool
        :type best_image: ndarray
        :type genome: Genome
        """
        if changes % self.frequency == 0:
            savefig(self.root + f"_fig{changes:04d}.png")
