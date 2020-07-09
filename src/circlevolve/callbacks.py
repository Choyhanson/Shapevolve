from utils import show_image

_display = None


def default_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                     complex_mutation, best_image, adjusters):
    global _display

    print(f"Total offspring: {offspring}")
    print(f"Total changes: {changes}")
    print(f"Total loop iterations: {loop_index}")
    print(f"Total mutation type switches: {num_mutation_type_switches}")
    print(f"Current error: {error}")
    extreme = "Yes" if complex_mutation else "No"
    print(f"Is currently in a complex mutation: {extreme}")

    if _display is None:
        _display = show_image(best_image, adjusters=adjusters)
    else:
        show_image(best_image, display=_display, adjusters=adjusters)


def quiet_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                   complex_mutation, best_image, adjusters):
    if changes % 50 == 0:
        default_callback(offspring, changes, loop_index, num_mutation_type_switches, error,
                         complex_mutation, best_image, adjusters)
