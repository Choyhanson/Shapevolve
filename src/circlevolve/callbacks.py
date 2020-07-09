import csv

import cv2

from utils import show_image

_display = None


def default_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                     complex_mutation, best_image, genome):
    visual_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                    complex_mutation, best_image, genome)


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
def visual_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                    complex_mutation, best_image, genome):
    _visualize(best_image, genome.adjusters, changes)


def quiet_visual_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                          complex_mutation, best_image, genome):
    if changes % 50 == 0:
        visual_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                        complex_mutation, best_image, genome)


# noinspection PyUnusedLocal,PyUnusedLocal
def verbose_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                     complex_mutation, best_image, genome):
    print(f"Total offspring: {offspring}")
    print(f"Total changes: {changes}")
    print(f"Total loop iterations: {loop_index}")
    print(f"Total mutation type switches: {num_mutation_type_switches}")
    print(f"Current error: {error}")
    extreme = "Yes" if complex_mutation else "No"
    print(f"Is currently in a complex mutation: {extreme}")


def quiet_verbose_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                           complex_mutation, best_image, genome):
    if changes % 50 == 0:
        verbose_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                         complex_mutation, best_image, genome)


def _visualize(best_image, adjusters, changes):
    global _display
    if _display is None:
        _display = show_image(best_image, changes, adjusters=adjusters)
    else:
        show_image(best_image, changes, display=_display, adjusters=adjusters)


class GenomeSaver:
    def __init__(self, genome_root):
        self.root = genome_root

    def callback(self, offspring, changes, loop_index, num_mutation_type_switches, error,
                 complex_mutation, best_image, genome):
        genome.save_genome(self.root + f"_gen{changes}.genome")


class QuietGenomeSaver(GenomeSaver):
    def callback(self, offspring, changes, loop_index, num_mutation_type_switches, error,
                 complex_mutation, best_image, genome):
        if changes % 50 == 0:
            GenomeSaver.callback(self, offspring, changes, loop_index, num_mutation_type_switches, error,
                                 complex_mutation, best_image, genome)


class CSVLogger:
    def __init__(self, csv_root):
        self.root = csv_root
        with open(csv_root, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["offspring", "generation", "loop_index", "error"])

    def callback(self, offspring, changes, loop_index, num_mutation_type_switches, error,
                 complex_mutation, best_image, genome):
        with open(self.root, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([offspring, changes, loop_index, error])


class QuietCSVLogger(CSVLogger):
    def callback(self, offspring, changes, loop_index, num_mutation_type_switches, error,
                 complex_mutation, best_image, genome):
        if changes % 50 == 0:
            CSVLogger.callback(self, offspring, changes, loop_index, num_mutation_type_switches, error,
                               complex_mutation, best_image, genome)


class ImageSaver:
    def __init__(self, image_root):
        self.root = image_root

    def callback(self, offspring, changes, loop_index, num_mutation_type_switches, error,
                 complex_mutation, best_image, genome):
        if not cv2.imwrite(self.root + f"_img{changes}.png", best_image):
            raise FileNotFoundError("The path given to ImageSaver was not valid.")


class QuietImageSaver(ImageSaver):
    def callback(self, offspring, changes, loop_index, num_mutation_type_switches, error,
                 complex_mutation, best_image, genome):
        if changes % 50 == 0:
            ImageSaver.callback(self, offspring, changes, loop_index, num_mutation_type_switches, error,
                                complex_mutation, best_image, genome)


class HighQualityImageSaver(ImageSaver):
    def callback(self, offspring, changes, loop_index, num_mutation_type_switches, error,
                 complex_mutation, best_image, genome):
        image = genome.render_scaled_image()
        ImageSaver.callback(self, offspring, changes, loop_index, num_mutation_type_switches, error,
                            complex_mutation, image, genome)


class QuietHighQualityImageSaver(HighQualityImageSaver):
    def callback(self, offspring, changes, loop_index, num_mutation_type_switches, error,
                 complex_mutation, best_image, genome):
        if changes % 50 == 0:
            HighQualityImageSaver.callback(self, offspring, changes, loop_index, num_mutation_type_switches, error,
                                           complex_mutation, best_image, genome)
