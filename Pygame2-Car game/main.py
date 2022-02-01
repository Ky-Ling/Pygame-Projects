'''
Date: 2021-10-23 19:21:09
LastEditors: GC
LastEditTime: 2022-02-01 22:40:01
FilePath: \Pygame2-Car game\main.py
'''


import os
import time
import math
import pygame
from utils import scale_image, blit_rotate_center, blit_text_center


pygame.font.init()

# Load all the images
GRASS = scale_image(pygame.image.load(
    os.path.join("imgs", "grass.jpg")), 2.5)
TRACK = scale_image(pygame.image.load(
    os.path.join("imgs", "track.png")), 0.9)

TRACK_BORDER = scale_image(pygame.image.load(
    os.path.join("imgs", "track-border.png")), 0.9)


# We will make the track-border as our mask, this will be one mask, and then we will compare this to the player car, and we
#   will see if these two masks are colliding with each other.

# How to create the mask:
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load(
    os.path.join("imgs", "finish.png"))
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130, 250)

RED_CAR = scale_image(pygame.image.load(
    os.path.join("imgs", "red-car.png")), 0.55)
GREEN_CAR = scale_image(pygame.image.load(
    os.path.join("imgs", "green-car.png")), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()

# Creating the pygame window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Give this window a name
pygame.display.set_caption("Racing game!")

MAIN_FONT = pygame.font.SysFont("comicsans", 44)

FPS = 60
PATH = [(176, 142), (105, 75), (57, 171), (59, 458), (287, 710), (406, 627), (430, 509), (568, 501), (600, 657), (668, 730), (741, 611), (740, 409),
        (603, 369), (438, 364), (436, 263), (586, 257), (711, 253), (739, 163), (697, 78), (340, 72), (276, 190), (271, 382), (170, 350), (171, 262)]


class GameInfo:
    LEVELS = 10

    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0

    def next_level(self):
        self.level += 1

        # If we are going to the next level, we do not wanna start the next level yet, we need to wait to user to do that.
        self.started = False

    # Reset everything
    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    # If the current level is greater than however many levels we have, and then we will finish the game.
    def game_finished(self):
        return self.level > self.LEVELS

    # Keep the track of when the level started, and then we can easily determine how much time has elapsed by checking the
    #   current time
    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)


# Handle all the stuff about the car.
# Put all the common stuff about the player car and computer car in this abstract class, it serves as the base class for
#   these two cars.
class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS

        # Every time we press down the "w", we are going to increase the velocity of the car by 0.1.
        self.acceleration = 0.1

    # Rotate the car:

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    # Make a function to draw the car for us:
    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    # Increase the velocity of the car based on the acceleraion, and if we are on the max velocity, we won't do anything.
    def move_forward(self):
        # If self.vel is already at the max velocity, and we add self.acceleration, we do not wanna go faster than max_vel.
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        # "-self.max_vel/2 " means when you go reverse, you are going to slower.
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)

        # The offset is relative to the calling mask.
        # We will take whatever our current x and y position is, and we are going to substract that from the x and y from the
        #   other mask. New that will give us the displacement between the two masks.

        offset = (int(self.x - x), int(self.y - y))

        # "poi" stands for "point of intersection"
        poi = mask.overlap(car_mask, offset)

        # If there is no poi, the two objects did not collide, if there was a poi, then they did collide.
        return poi

    # Reset our car position, like prepare for the next level
    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0


class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180, 200)

    # Slowing down the car:
    def reduce_speed(self):
        # If the result of (self.vel - self.acceleration / 2) is negative, we do not wanna move backwards, we just wanna stop.
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    # New we need to do a bounce, when our car hit the wall, we are going to bounce off the wall with the same velocity.
    def bounce(self):
        # Reverse the velocity:
        self.vel = -self.vel
        self.move()


class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)

    # Override
    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        # Path is going to be a list of coordinates of points that I wanna my car move to.
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            # point means the center of the circle
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    # Override the draw method of AbstractCar class.
    def draw(self, win):
        super().draw(win)
        # self.draw_points(win)

    # It is going to calculate the angle and shift our car in that direction
    def calculate_angle(self):
        # Calculate the displacement in x and y between the target point in my current point. Then I can find the angel between my
        #   car and the point, and then i can just the position of angle of my car accordingly to move towards that target point.
        target_x, target_y = self.path[self.current_point]

        # Calculate the difference
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        # If we do not have difference in y, that means we are horizontal.
        if y_diff == 0:
            desired_radian_angle = math.pi/2
        else:
            # It will give me the angle between the car and the point.
            desired_radian_angle = math.atan(x_diff/y_diff)

        # If the target we are looking for is actually lower down on the screen, we will go a complete opposite direction of what
        #   the angel that we calculated.
        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)

        # If the difference in the angle is larger than 180 degrees, we will take an ineffective route to get to the angle.
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        # New we just wanna move in the right direction to get towards that we want.
        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    # To see if we need to move to the next point, because as soon as we hit the point, we collide with that point, and
    #   then we will move to the next one.
    # Make sure that we move to the next point in our path when we are ready to do that.

    def update_path_point(self):
        # Check for a collosion with the points that we have
        target = self.path[self.current_point]

        # Create a rectangle from the car based on the x and y position and get the width and height.
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())

        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        # Make sure we have a point to move. It is going to ensure that we are not going to get an index error by trying to
        #   move to a point that does not exist.
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()

        # Override the move method
        super().move()

    # Update the speed based on the current level
    def next_level(self, level):
        # When we go to the next level, we need to reset this car.
        self.reset()

        # After we reset the car, we need to change the velocity base on the levels. And one thing keep in mind is that we do
        #   not wanna the computer car faster than the player car.
        self.vel = self.max_vel + (level - 1) * 0.2

        self.current_point = 0


def draw(win, images, player_car, computer_car, game_info):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    computer_car.draw(win)

    # Render some text and draw some stats onto the screen
    level_text = MAIN_FONT.render(
        f"Level {game_info.level}", 1, (255, 255, 255))
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 70))

    time_text = MAIN_FONT.render(
        f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255))
    win.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))

    vel_text = MAIN_FONT.render(
        f"Vel: {round(player_car.vel, 1)}px/s", 1, (255, 255, 255))
    win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 10))

    # You can draw a bunch of stuff, and then as soon as you have drawn it on the screen, you update the display and then it
    #   will show all of the stuff you have drawn.
    pygame.display.update()


def move_player(player_car):
    # Key presses and turing:
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        # To make sure we do not reduce our speed as we are going forward.
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()


def handle_collision(player_car, computer_car, game_info):
    # Check for this collision
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    computer_finish_poi_collide = computer_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    if computer_finish_poi_collide != None:
        blit_text_center(WIN, MAIN_FONT, "You lost !")

        pygame.display.update()
        # If you lose this game, you have to wait for 5s and the we will reset the game.
        pygame.time.wait(5000)
        game_info.reset()
        computer_car.reset()
        player_car.reset()

    # But in this game,if we drive backwards, we do not wanna be able to go past the finish line, we should only be able to
    #   go forward on the track. So we are going to use the point of the intersection to determine what direction i hit to
    #   finish line from.
    player_finish_poi_collide = player_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    if player_finish_poi_collide != None:

        # What we can do is to check if the y coodinate of the poi is 0, and if it is 0, that means we hit
        #   it from the top, if it is not, it means we hit it from the bottom and we actually finished(meaning we are all
        #   the way around the track.)
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()

        # And new we are going to implement what happends if we cross the finish line from the correct direction.
        else:
            game_info.next_level()
            player_car.reset()
            # If the computer car wins, we will call the next_level function
            computer_car.next_level(game_info.level)


run = True

images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
          (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]


player_car = PlayerCar(2, 4)
computer_car = ComputerCar(2, 4, PATH)

game_info = GameInfo()

# We need to set up a clock, it will make sure our window is not going to run faster than a certain frame per second.
clock = pygame.time.Clock()

# Rotating the car
while run:

    clock.tick(FPS)

    draw(WIN, images, player_car, computer_car, game_info)

    # We draw everything on the screen, and then we will have this while loop, this is only going to run if we have not started
    #  the current level. And if we have not started the current level, we will draw some text in the middle of the screen, and
    #   then as soon as they press the any key down, and then we will start the current level.
    while not game_info.started:
        # If we do not start the current level, we will blit some text on the screen
        blit_text_center(
            WIN, MAIN_FONT, f"Press any key to start level {game_info.level} !! ")
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN:
                game_info.start_level()

    # Make a event to keep this window alive, keep it running on the screen. And as soon as you quit the window or the game ends,
    #   that you would destory the event loop and destory the game and the window will disappear.

    # Give us a list of events and we can loop through them
    for event in pygame.event.get():

        # The first event we wanna check is if the user close the window
        if event.type == pygame.QUIT:
            run = False
            break

        # # Create a path
        # # Click with the mouse, and adds a point to our computer path, and we can get all of the points at the end of the program,
        # #   so we do not have to manually write them.
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     # Get the position of the mouse, it will give us the x and y coodinate of our mouse on the pygame screen
        #     pos = pygame.mouse.get_pos()

        #     # Add that position to the computer's path
        #     computer_car.path.append(pos)

        # # After we run this program and get the position points, we need to create a variable called PATH, and pass a parameter
        # #   to the computer_car.
    move_player(player_car)

    computer_car.move()

    handle_collision(player_car, computer_car, game_info)

    if game_info.game_finished():
        blit_text_center(WIN, MAIN_FONT, "You won the game!")
        pygame.time.wait(5000)
        game_info.reset()
        computer_car.reset()
        player_car.reset()


# print(computer_car.path)
pygame.quit()
