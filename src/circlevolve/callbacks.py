from utils import show_image

display = None


def default_callback(offspring, changes, generation_index, total_generation_changes, top_score,
                     extreme_mutation, top_image, adjusters):
    global display

    print(f"offspring: {offspring}")
    print(f"number of changes: {changes}")
    print(f"number of total generations: {generation_index}")
    print(f"number of evolution switches: {total_generation_changes}")
    print(f"error: {top_score}")
    extreme = "extreme" if extreme_mutation else "not extreme"
    print(f"Extreme?: {extreme}")

    if display is None:
        display = show_image(top_image, adjusters=adjusters)
    else:
        show_image(top_image, display=display, adjusters=adjusters)


def quiet_callback(offspring, changes, generation_index, total_generation_changes, top_score,
                   extreme_mutation, top_image, adjusters):
    if changes % 50 == 0:
        default_callback(offspring, changes, generation_index, total_generation_changes, top_score,
                         extreme_mutation, top_image, adjusters)
