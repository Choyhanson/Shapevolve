import time
from math import inf  # for math help :D
from multiprocessing import Pool  # To distribute processesh

# noinspection PyUnresolvedReferences
import cv2  # opencv2 for image management
# noinspection PyUnresolvedReferences
import numpy as np  # for linear algebra help
from PIL import Image  # for initial image palette and bgcolor generation with help of colorthief
from matplotlib.pyplot import show

# noinspection PyUnresolvedReferences
from adjusters import NO_ADJUSTER
from colorthief_from_image import ColorThiefFromImage
# noinspection PyUnresolvedReferences
from error_metrics import mean_squared_error
from gene import Gene
from genome import Genome
from mutations import simple_mutation, complex_mutation
# noinspection PyUnresolvedReferences
from preprocessors import smooth_preprocess
from utils import get_rescale_ratio, convert_RGB_to_BGR, show_image, add_circle


class Evolver:
    _EARLY_STOPPING_LIMIT = 25
    _EARLY_STOPPING_LIMIT_EXTREME = 200
    _SIMPLE_POOL_SIZE = 32
    _COMPLEX_POOL_SIZE = 4

    def __init__(self, filename, num_circles=1000, num_colors=256, target_resolution=250,
                 adjuster=NO_ADJUSTER, preprocess=smooth_preprocess,
                 calculate_error=mean_squared_error):

        self.filename = filename
        self.num_circles = num_circles
        self.num_colors = num_colors
        self.adjuster = adjuster
        self.calculate_error = calculate_error

        loaded_image = preprocess(Image.open(filename))

        self.ratio = get_rescale_ratio(loaded_image, target_resolution)
        self.width = int(loaded_image.width * self.ratio)
        self.height = int(loaded_image.height * self.ratio)
        loaded_image = loaded_image.resize((self.width, self.height), Image.LANCZOS)
        image_array = adjuster['adjust'](np.asarray(loaded_image))
        loaded_image = Image.fromarray(image_array)
        self.base_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        color_thief = ColorThiefFromImage(loaded_image)

        self.backgroundColor = convert_RGB_to_BGR(color_thief.get_color(quality=1))  # gets the background color

        # Gets the top colours used by the image
        self.palette = color_thief.get_palette(color_count=num_colors,
                                               quality=1)
        for index, color in enumerate(self.palette):
            self.palette[index] = convert_RGB_to_BGR(color)

        self.display = show_image(self.base_image)  # Preview image

        resolution = (self.width, self.height)
        self.minRadius = int(0.02 * min(resolution))
        self.maxRadius = int(0.08 * min(resolution))

        self.ancestorImage = np.zeros((self.height, self.width, 3), np.uint8)
        self.ancestorImage[:] = self.backgroundColor

        print("shape: ")
        print(self.base_image.shape)

        print("new shape: ")
        print(self.ancestorImage.shape)

    def evolve(self, num_generations=5000):
        top_score = inf  # original best score is infinite, so the first run will always overwrite it.
        top_image = None  # the best image so far.

        cached_image = None  # Location to store a cached image for later use.
        recall_from_cache = False  # Whether to load an image from the cache or build it from scratch.

        start = time.time()

        sequence = [Gene(self.maxRadius, self.minRadius, self.height, self.width, self.num_colors)
                    for _ in range(self.num_circles)]  # Generate initial gene sequence.

        genome = Genome(sequence, self.ratio, self.height, self.width,
                        self.backgroundColor, self.adjuster, self.palette)  # Build a genome

        generations_since_last_change = 0  # counter for above.
        total_generation_changes = 0  # number of total generation changes,
        # used to determine how long an algorithm should stay complex.
        consecutive_extreme_mutations = 0  # counter for early stopping.
        extreme_mutation = False  # default value of whether to use extreme mutations.

        final_run = False

        simple_pool = Pool(self._SIMPLE_POOL_SIZE)
        complex_pool = Pool(self._COMPLEX_POOL_SIZE)

        last_update = -1

        generation_index = 0
        offspring = 0  # Record number of generations.
        changes = 0  # Record number of total changes made.
        # (some generations may have failed mutations that do not affect the sequence.)

        print("start")

        while changes < num_generations:
            if extreme_mutation:
                final_run = False

                offspring += self._COMPLEX_POOL_SIZE

                results = complex_pool.starmap(complex_mutation, [
                    (self.ancestorImage, self.base_image, sequence, self.num_circles, self.calculate_error,
                     self.palette) for _ in range(self._COMPLEX_POOL_SIZE)])
                score_list = [results[index][0] for index in range(self._COMPLEX_POOL_SIZE)]
                best_index = score_list.index(min(score_list))
                score = results[best_index][0]
                mutated_gene = results[best_index][1]
                image = results[best_index][2]
                mutated_index = results[best_index][3]
                top = results[best_index][4]

                # If successful...
                if score < top_score:
                    top_score = score
                    top_image = image
                    del sequence[mutated_index]
                    if top:
                        sequence.append(mutated_gene)
                    else:
                        sequence.insert(mutated_index, mutated_gene)
                    changes += 1
                    # Reset all values and go back to regular mutations.
                    generations_since_last_change = 0
                    consecutive_extreme_mutations += 1
                    if consecutive_extreme_mutations >= total_generation_changes ** 2:
                        recall_from_cache = False
                        extreme_mutation = False
                else:
                    generations_since_last_change += 1
                    # If we really can't get anywhere, then quit.
                    if generations_since_last_change >= self._EARLY_STOPPING_LIMIT_EXTREME:
                        final_run = True
                        generations_since_last_change = 0
                        recall_from_cache = False
                        extreme_mutation = False

            else:

                offspring += self._SIMPLE_POOL_SIZE

                # add the rest of the circles normally
                if recall_from_cache:
                    image = cached_image.copy()  # Take built image from
                else:
                    image = self.ancestorImage.copy()
                    for index, gene in enumerate(sequence):
                        if index != 0:
                            add_circle(image, gene, self.palette)
                    cached_image = image.copy()
                    recall_from_cache = True

                results = simple_pool.starmap(simple_mutation,
                                              [(image, self.base_image, sequence, self.calculate_error, self.palette)
                                               for _ in range(self._SIMPLE_POOL_SIZE)])

                score_list = [results[index][0] for index in range(self._SIMPLE_POOL_SIZE)]
                best_index = score_list.index(min(score_list))
                score = results[best_index][0]
                mutated_gene = results[best_index][1]
                image = results[best_index][2]

                # if it was beneficial...
                if score < top_score:
                    top_score = score
                    top_image = image

                    del sequence[0]
                    sequence.append(mutated_gene)  # Place the gene on top of the sequence again.

                    changes += 1  # record a change
                    generations_since_last_change = 0
                    recall_from_cache = False  # Build next image from scratch.
                    final_run = False
                else:
                    generations_since_last_change += 1
                    if generations_since_last_change >= self._EARLY_STOPPING_LIMIT:
                        total_generation_changes += 1
                        extreme_mutation = True
                        generations_since_last_change = 0
                        consecutive_extreme_mutations = 0
                        if final_run:
                            break

            generation_index += 1

            # Periodic checks on progress, every 100 generations.
            if changes % 50 == 0 and last_update != changes:
                last_update = changes
                print(f"offspring: {offspring}")
                print(f"number of changes: {changes}")
                print(f"number of total generations: {generation_index}")
                print(f"number of evolution switches: {total_generation_changes}")
                print(f"error: {top_score}")
                extreme = "extreme" if extreme_mutation else "not extreme"
                print(f"Extreme?: {extreme}")
                show_image(top_image, display=self.display, adjuster=self.adjuster)

        end = time.time()
        print(f"Total time elapsed: {end - start}")

        image = genome.render_scaled_image()
        show_image(genome.render_scaled_image(), display=self.display, adjuster=genome.adjuster)
        cv2.imwrite(self.filename + "_result.png", image)
        genome.save_genome(self.filename + "_genome.pkl")

        print("changes: ")
        print(changes)
        show()

        return genome
