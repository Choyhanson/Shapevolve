from utils import show_image

_display = None


def default_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                     complex_mutation, best_image, adjusters):
    visual_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                    complex_mutation, best_image, adjusters)


def visual_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                    complex_mutation, best_image, adjusters):
    _visualize(best_image, adjusters, changes)


def quiet_visual_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                          complex_mutation, best_image, adjusters):
    if changes % 50 == 0:
        visual_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                        complex_mutation, best_image, adjusters)


def verbose_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                     complex_mutation, best_image, adjusters):
    print(f"Total offspring: {offspring}")
    print(f"Total changes: {changes}")
    print(f"Total loop iterations: {loop_index}")
    print(f"Total mutation type switches: {num_mutation_type_switches}")
    print(f"Current error: {error}")
    extreme = "Yes" if complex_mutation else "No"
    print(f"Is currently in a complex mutation: {extreme}")


def quiet_verbose_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                           complex_mutation, best_image, adjusters):
    if changes % 50 == 0:
        verbose_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                         complex_mutation, best_image, adjusters)


def _visualize(best_image, adjusters, changes):
    global _display
    if _display is None:
        _display = show_image(best_image, changes, adjusters=adjusters)
    else:
        show_image(best_image, changes, display=_display, adjusters=adjusters)
