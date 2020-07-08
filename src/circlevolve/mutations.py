from random import randint, random


def simple_mutation(image, base_image, sequence, calculate_error, palette, draw):  # Computes the effects of a simple
    # mutation.
    mutated_gene = sequence[0].clone()
    mutated_gene.mutate()
    new_image = image.copy()
    draw(new_image, mutated_gene, palette)
    error = calculate_error(new_image, base_image)
    return error, mutated_gene, new_image


def complex_mutation(ancestor_image, base_image, sequence, num_circles, calculate_error,
                     palette, draw):  # computes the effects of a complex mutation.

    mutation_index = randint(0, num_circles - 1)
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
