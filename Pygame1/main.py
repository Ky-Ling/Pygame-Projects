'''
Date: 2021-09-07 16:23:39
LastEditors: GC
LastEditTime: 2021-12-22 10:59:24
FilePath: \Pygame1\main.py
'''

# 1: Make the main surface and draw the window --> pygame.draw.rect(WIN, BLACK, BORDER)
# 2: Control the speed of the while loop --> clock = pygame.time.Clock()
# 3: Get the event from the queue --> for event in pygame.event.get()
# 4: Define two rectangles to represent the spaceship --> yellow = pygame.Rect(700, 300, (SPACESHIP_WIDTH, SPACESHIP.HEIGHT))
# 5: Create two spaceships --> RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png")))
#                              RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)))
# 6: Draw the spaceships onto the screen: --> WIN.blit(RED_SPACESHIP, (red.x, red.y))

# 7: Make new functions to handle the movement of spaceships:
#        get the keys from the keyboard: key_pressed = pygame.key.get_pressed()
# 8: In the main function, we should create bullets and press the key downsides:
# 9: In the draw_window function, we should create bullets onto the screen: for bullet in red_bullets:pygame.draw.rect(WIN, RED, bullet)
# 10: We also have to create a new function to handle the bullets:
#      (1): We will loop over all the yellow bullets and check if they have collided with the end of the screen or with the red charactor.
#            for bullet in red_bullets: bullet -+ BULLET_VEL
#      (2): Check the collision:
#           if yellow.colliderect(bullet):
#                pygame.event.post(pygame.event.Event(YELLOW_HIT))
#                red_bullets.remove(bullet)
#           elif bullet.x < 0: red_bullets.remove(bullet)

# 11: We have to create the font that we wanna use: HEALTH_FONT = pygame.font.SysFont("")  WINNER_FONT = pygame.SysFont()
# 12: We have to create a function to draw the winner text: draw_text = WINNER_FONT.render(text, 1, WHITE)
#                                                           WIN.blit(draw_text, (HEIGHT / 2 - draw_text.get_height / 2, WIDTH / 2 - draw_text.get_width / 2))
# 13: We also have to draw the health font of the spaceship in the draw_window function:
#     red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
#     WIN.blit(red_health_text, (WIDTH - red_health_text.get_width - 10, 10))
# 14: In the main function, we have to get the winner_text:
#     winner_text = ""
#     if red_health <= 0:
#         print("Yellow Wins!!!")


import pygame
import os
pygame.init()

# Initialize the pygame font library or whatever it may be
pygame.font.init()

pygame.mixer.init()


# Make the main surface
WIDTH, HEIGHT = 900, 500

# Make a new window with the width and height:
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Change the name of the pygame window:
pygame.display.set_caption("First Funny Game! ")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# It will define how quickly or how many frames per second, we wanna our game to update at.
FPS = 60

# Make a rectangle which is a border and divide the middle of this screen.
# pygame.Rect(left, top, width, height)
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

# Load in a mixer sound which will allow us to start or stop a sound whenever we want.
# BULLET_HIT_SOUND = pygame.mixer.Sound(
#     os.path.join("Assets", "Grenade+1.mp3"))
# BULLET_FIRE_SOUND = pygame.mixer.Sound(
#     os.path.join("Assets", "Gun+Silencer.mp3"))


# Define the font that i wanna use.
HEALTH_FONT = pygame.font.SysFont("SanFrancisco", 40)
WINNER_FONT = pygame.font.SysFont("SanFrancisco", 100)

VEL = 5

# We have to decide how fast we want these bullets to go, we wanna make it faster than the charactors.
BULLET_VEL = 7

# We wanna make sure each player has a finite number of bullets
MAX_BULLETS = 3

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# This just represent the code or the number for a custom user event, since we are going to have multiple user events, we
# can add one to the yellow_hit and add two to the red_hit. So now we have two separate events that we can check for and handle.
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # Fill the screen with the specific color:
    WIN.blit(SPACE, (0, 0))

    # we draw the window and its color is black, and give this window a border:
    pygame.draw.rect(WIN, BLACK, BORDER)

    # Draw their scores or their health on the screen:
    # We are using the HEALTH_FONT to render some texts
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # Use blit to when you want to draw a surface onto the screen
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # Draw the bullets onto the screen
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


# How can we can not across the border? Like yellow.x - VEL > 0
def yellow_handle_movement(keys_pressed, yellow):

    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        # Move the spaceship to the left.
        yellow.x -= VEL

    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        # Move the spaceship to the right
        yellow.x += VEL

    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        # Move the spaceship to the up
        yellow.y -= VEL

    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 10:
        # Move the spaceship to the down
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):

    if keys_pressed[pygame.K_LEFT] and red.x - VEL - 15 > BORDER.x + BORDER.width:
        # Move the spaceship to the left.
        red.x -= VEL

    if keys_pressed[pygame.K_RIGHT] and red.x + red.width < WIDTH + 10:
        # Move the spaceship to the right
        red.x += VEL

    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        # Move the spaceship to the up
        red.y -= VEL

    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 10:
        # Move the spaceship to the down
        red.y += VEL

# We need to move the bullets and we need to see if they hit any of the charactors, handle the collision of the bullets and handle
# the removing bullets when they get off the screen or collide with a charactor.


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    # We will loop over all the yellow bullets and check if they have collided with the end of the screen or with the red charactor.
    for bullet in yellow_bullets:
        # Move the bullets:
        bullet.x += BULLET_VEL

        # Check the collision:
        # This method is to check if it'd be rectangle representing our yellow charactor has collided with the rectangle representing
        # our bullets

        # We are checking if the yellow bullets hitting the red charactors, so we use red.collidedict()
        if red.colliderect(bullet):
            # We have to create a new event, and we can check for that event inside of the while loop of the main function and do something if
            # that event occurs.
            pygame.event.post(pygame.event.Event(RED_HIT))

            # If we collide the yellow charactor, the first thing we need to do is to remove this bullet.
            yellow_bullets.remove(bullet)

        # After we checked the collide rectangle, we need to check if any of these bullets are off the screen
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(
        draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))

    pygame.display.update()
    pygame.time.delay(5000)


def main():

    # We will define two rectangles which are going to represent my yellow spaceship and red spaceship so that i can control
    # where they are moving to.
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # It will store all the yellow players bullets and the red players bullets.
    yellow_bullets = []
    red_bullets = []

    red_health = 15
    yellow_health = 15

    # To control the speed of this while loop, it will make sure that we are gonna run this while loop here 60 times per second.
    clock = pygame.time.Clock()

    run = True
    while run:
        # To ensure that we never go over this capped frame rate of 60.
        clock.tick(FPS)

        for event in pygame.event.get():
            # The first event is that we wanna check is if the user quit the window.
            if event.type == pygame.QUIT:
                run = False

            # Make a way to create a bullet and have it kind of fire around the screen.
            # We pressed a key downwards:
            if event.type == pygame.KEYDOWN:
                # We need to check whether we pressed the left control or the right control.
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    # Then create a bullet for our charactor
                    # We are going to create a rectangle that is add a position that we want to fire it from.
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()

            # We wanna have both charactors have some number of health and every time they get hit, that is obvious get
            # substract.
            if event.type == RED_HIT:
                red_health -= 1
                # BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                # BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow wins!!"
        if yellow_health <= 0:
            winner_text = "Red wins!!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        # Change the x and y position when we press the array keys, it will move base on the user input.
        # This method (pygame.key.get_pressed()) allows us to press the multiple keys at the same time.

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    pygame.quit()


if __name__ == "__main__":
    main()
