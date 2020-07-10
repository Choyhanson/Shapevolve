import cv2


def add_circle(image, gene, palette):  # Adds a circle based on gene info
    overlay = image.copy()
    cv2.circle(
        overlay,
        center=gene.center,
        radius=gene.radius,
        color=palette[gene.color],
        thickness=-1,
        lineType=cv2.LINE_AA  # add anti-aliasing
    )
    draw_overlay(image, overlay, gene.alpha)


def add_square(image, gene, palette):
    overlay = image.copy()
    point1 = (gene.center[0] - gene.radius, gene.center[1] - gene.radius)
    point2 = (gene.center[0] + gene.radius, gene.center[1] + gene.radius)
    cv2.rectangle(
        overlay,
        point1,
        point2,
        color=palette[gene.color],
        thickness=-1,
        lineType=cv2.LINE_AA
    )
    cv2.addWeighted(overlay, gene.alpha, image, 1 - gene.alpha, 0, image)
    draw_overlay(image, overlay, gene.alpha)


def draw_overlay(image, overlay, alpha):
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
