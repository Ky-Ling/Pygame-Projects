
import pygame


def scale_image(img, factor):
    # We will get a tuple, that contains new width and the new height of our image.
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


# Take a image and return to a rotate image based on an angle
def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    # Get a rectangle from the new_rect, and make its center equal to the original image, and we are saying the top left corner
    #   of that original image is equal to whatever the X and Y position is. And the new image need to still be on the same center.
    #   So we are just rotate the center of the image, not the top left of the image.

    # To find the correct X and Y position of the new rectangle.
    win.blit(rotated_image, new_rect.topleft)

 # Create a function that is capable of writing any text on to the screen directly in the center of the screen


def blit_text_center(win, font, text):
    render = font.render(text, 1, (200, 200, 200))
    win.blit(render, (win.get_width()/2 - render.get_width() /
                      2, win.get_height()/2 - render.get_height()/2))
