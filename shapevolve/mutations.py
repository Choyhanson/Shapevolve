"""Defines mutations."""

from random import randint, random


def simple_mutation(image, base_image, sequence, calculate_error, palette, draw):
    """Computes the effects of a simple mutation.

    :param image: The image to draw the gene on.
    :param base_image: The original image to compare to.
    :param sequence: The gene sequence.
    :param calculate_error: The error metric method.
    :param palette: The color palette to use.
    :param draw: The method to draw the shape according to the gene.
    :type image: ndarray
    :type base_image: ndarray
    :type sequence: List[Gene]
    :type calculate_error: Callable
    :type palette: List[Tuple[int, int, int]]
    :type draw: Callable
    :return: The error, the mutated gene, and the new image.
    :rtype: Tuple[float, Gene, ndarray]
    """
    mutated_gene = sequence[0].clone()
    mutated_gene.mutate()
    new_image = image.copy()
    draw(new_image, mutated_gene, palette)
    error = calculate_error(new_image, base_image)
    return error, mutated_gene, new_image


def complex_mutation(ancestor_image, base_image, sequence, num_shapes, calculate_error, palette, draw):
    """Computes the effects of a complex mutation.

    :param ancestor_image: An image with the solid background color only.
    :param base_image: The original image for comparison.
    :param sequence: The existing gene sequence.
    :param num_shapes: The number of shapes to draw.
    :param calculate_error: The error metric method.
    :param palette: The color palette to use.
    :param draw: The method to draw the shape according to the gene.
    :type ancestor_image: ndarray
    :type base_image: ndarray
    :type sequence: List[Gene]
    :type num_shapes: int
    :type calculate_error: Callable
    :type palette: List[Tuple[int, int, int]]
    :type draw: Callable
    :return: The error, the mutated gene, the new image, the index of the mutated gene, whether mutated gene was placed on top.
    :rtype: Tuple[float, Gene, ndarray, int, bool]
    """
    mutation_index = randint(0, num_shapes - 1)
    mutated_gene = sequence[mutation_index].clone()
    mutated_gene.mutate()

    new_image = ancestor_image.copy()

    if random() > 0.5:
        for index, gene in enumerate(sequence):
            if index != mutation_index:
                draw(new_image, gene, palette)
        draw(new_image, mutated_gene, palette)
        top = True

    else:
        for index, gene in enumerate(sequence):
            if index == mutation_index:
                draw(new_image, mutated_gene, palette)
            else:
                draw(new_image, gene, palette)
        top = False

    error = calculate_error(new_image, base_image)
    return error, mutated_gene, new_image, mutation_index, top
