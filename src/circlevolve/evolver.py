from multiprocessing import Pool  # To distribute processes

# noinspection PyUnresolvedReferences
import cv2  # opencv2 for image management
# noinspection PyUnresolvedReferences
import numpy as np  # for linear algebra help
from PIL import Image  # for initial image palette and bgcolor generation with help of colorthief

# noinspection PyUnresolvedReferences
from adjusters import adjust
# noinspection PyUnresolvedReferences
from callbacks import default_callback
from colorthief_from_image import ColorThiefFromImage
from drawers import add_circle
# noinspection PyUnresolvedReferences
from error_metrics import mean_squared_error
from gene import Gene
from genome import Genome
from mutations import simple_mutation, complex_mutation
# noinspection PyUnresolvedReferences
from preprocessors import smooth_preprocess
from utils import get_rescale_ratio, convert_RGB_to_BGR


class Evolver:
    _EARLY_STOPPING_LIMIT = 25
    _EARLY_STOPPING_LIMIT_EXTREME = 200
    _SIMPLE_POOL_SIZE = 32
    _COMPLEX_POOL_SIZE = 4

    def __init__(self, filepath, saved_genome=None, num_circles=1000, num_colors=256, target_resolution=250,
                 adjusters=None, preprocesses=None, draw=add_circle, calculate_error=mean_squared_error):
        if adjusters is None:
            self.adjusters = []
        else:
            self.adjusters = adjusters

        if preprocesses is None:
            preprocesses = [smooth_preprocess]

        self.draw = draw
        self.num_circles = num_circles
        self.num_colors = num_colors
        self.calculate_error = calculate_error

        loaded_image = Image.open(filepath)
        for preprocess in preprocesses:
            loaded_image = preprocess(loaded_image)

        self.ratio = get_rescale_ratio(loaded_image, target_resolution)
        self.width = int(loaded_image.width * self.ratio)
        self.height = int(loaded_image.height * self.ratio)
        loaded_image = loaded_image.resize((self.width, self.height), Image.LANCZOS)
        image_array = adjust(np.asarray(loaded_image), adjusters)

        loaded_image = Image.fromarray(image_array)
        self.base_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        color_thief = ColorThiefFromImage(loaded_image)

        background_color = convert_RGB_to_BGR(color_thief.get_color(quality=1))  # gets the background color

        # Gets the top colours used by the image
        self.palette = color_thief.get_palette(color_count=num_colors, quality=1)
        for index, color in enumerate(self.palette):
            self.palette[index] = convert_RGB_to_BGR(color)

        resolution = (self.width, self.height)
        self.min_radius = int(0.02 * min(resolution))
        self.max_radius = int(0.08 * min(resolution))

        self.ancestor_image = np.zeros((self.height, self.width, 3), np.uint8)
        self.ancestor_image[:] = background_color

        self.sequence = [Gene(self.max_radius, self.min_radius, self.height, self.width, self.num_colors)
                         for _ in range(self.num_circles)]  # Generate initial gene sequence.

        self.genome = Genome(self.sequence, self.ratio, self.height, self.width,
                             background_color, self.adjusters, self.palette, self.draw)  # Build a genome

        if saved_genome is not None:
            if Genome.isCompatible(self.genome, saved_genome):
                self.genome = saved_genome
                self.sequence = saved_genome.sequence

    def evolve(self, num_generations=5000, callbacks=None):

        if callbacks is None:
            callbacks = [default_callback]

        cached_image = None  # Location to store a cached image for later use.
        recall_from_cache = False  # Whether to load an image from the cache or build it from scratch.

        num_consecutive_failed_loops = 0  # counter for above.
        num_mutation_type_switches = 0  # number of total generation changes,
        # used to determine how long an algorithm should stay complex.
        num_complex_mutation_successes_since_switch = 0  # counter for early stopping.
        use_complex_mutation = False  # default value of whether to use extreme mutations.

        final_run = False

        simple_pool = Pool(self._SIMPLE_POOL_SIZE)
        complex_pool = Pool(self._COMPLEX_POOL_SIZE)

        previous_changes = -1

        loop_index = 0
        offspring = 1  # Record number of generations.
        changes = 0  # Record number of total changes made.
        # (some generations may have failed mutations that do not affect the sequence.)

        best_image = self.genome.render_raw_image()
        best_error = self.calculate_error(best_image, self.base_image)

        for callback in callbacks:
            callback(offspring, changes, loop_index, num_mutation_type_switches, best_error,
                     use_complex_mutation, best_image, self.genome.adjusters)

        while changes < num_generations:
            if use_complex_mutation:
                final_run = False

                offspring += self._COMPLEX_POOL_SIZE

                results = complex_pool.starmap(complex_mutation, [
                    (self.ancestor_image, self.base_image, self.sequence, self.num_circles, self.calculate_error,
                     self.palette, self.draw) for _ in range(self._COMPLEX_POOL_SIZE)])
                error_list = [results[index][0] for index in range(self._COMPLEX_POOL_SIZE)]
                best_index = error_list.index(min(error_list))
                error = results[best_index][0]
                mutated_gene = results[best_index][1]
                image = results[best_index][2]
                mutated_index = results[best_index][3]
                is_top_mutation = results[best_index][4]

                # If successful...
                if error < best_error:
                    best_error = error
                    best_image = image
                    del self.sequence[mutated_index]
                    if is_top_mutation:
                        self.sequence.append(mutated_gene)
                    else:
                        self.sequence.insert(mutated_index, mutated_gene)
                    changes += 1
                    # Reset all values and go back to regular mutations.
                    num_consecutive_failed_loops = 0
                    num_complex_mutation_successes_since_switch += 1
                    if num_complex_mutation_successes_since_switch >= num_mutation_type_switches ** 2:
                        recall_from_cache = False
                        use_complex_mutation = False
                else:
                    num_consecutive_failed_loops += 1
                    # If we really can't get anywhere, then quit.
                    if num_consecutive_failed_loops >= self._EARLY_STOPPING_LIMIT_EXTREME:
                        final_run = True
                        num_consecutive_failed_loops = 0
                        recall_from_cache = False
                        use_complex_mutation = False

            else:
                offspring += self._SIMPLE_POOL_SIZE

                # add the rest of the circles normally
                if recall_from_cache:
                    image = cached_image.copy()  # Take built image
                else:
                    image = self.ancestor_image.copy()
                    for index, gene in enumerate(self.sequence):
                        if index != 0:
                            self.draw(image, gene, self.palette)
                    cached_image = image.copy()
                    recall_from_cache = True

                results = simple_pool.starmap(simple_mutation,
                                              [(image, self.base_image, self.sequence, self.calculate_error,
                                                self.palette, self.draw) for _ in range(self._SIMPLE_POOL_SIZE)])

                error_list = [results[index][0] for index in range(self._SIMPLE_POOL_SIZE)]
                best_index = error_list.index(min(error_list))
                error = results[best_index][0]
                mutated_gene = results[best_index][1]
                image = results[best_index][2]

                # if it was beneficial...
                if error < best_error:
                    best_error = error
                    best_image = image

                    del self.sequence[0]
                    self.sequence.append(mutated_gene)  # Place the gene on top of the sequence again.

                    changes += 1  # record a change
                    num_consecutive_failed_loops = 0
                    recall_from_cache = False  # Build next image from scratch.
                    final_run = False
                else:
                    num_consecutive_failed_loops += 1
                    if num_consecutive_failed_loops >= self._EARLY_STOPPING_LIMIT:
                        num_mutation_type_switches += 1
                        use_complex_mutation = True
                        num_consecutive_failed_loops = 0
                        num_complex_mutation_successes_since_switch = 0
                        if final_run:
                            break

            loop_index += 1

            if previous_changes != changes:
                previous_changes = changes
                for callback in callbacks:
                    callback(offspring, changes, loop_index, num_mutation_type_switches, best_error,
                             use_complex_mutation, best_image, self.genome.adjusters)

        simple_pool.close()
        simple_pool.join()

        complex_pool.close()
        complex_pool.join()

        return self.genome, self.genome.render_scaled_image()
