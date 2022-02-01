'''
Date: 2021-10-24 18:58:51
LastEditors: GC
LastEditTime: 2021-10-28 15:16:35
FilePath: \Pygame2-Car game\practice.py
'''
import pygame
import time
import math
import os

from pygame.constants import MOUSEBUTTONDOWN
from utils import blit_rotate_center, scale_image

GRASS = scale_image(pygame.image.load(os.path.join("imgs", "grass.jpg")), 2.5)

TRACK = scale_image(pygame.image.load(os.path.join("imgs", "track.png")), 0.9)

TRACK_BORDER = scale_image(pygame.image.load(
    os.path.join("imgs", "track-border.png")), 0.9)

TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load(os.path.join("imgs", "finish.png"))
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130, 250)

RED_CAR = scale_image(pygame.image.load(
    os.path.join("imgs", "red-car.png")), 0.55)

GREEN_CAR = scale_image(pygame.image.load(
    os.path.join("imgs", "green-car.png")), 0.55)


WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()


WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("New Car Racing!")

PATH = [(175, 165), (160, 93), (78, 96), (60, 446), (304, 720), (403, 695), (404, 559), (502, 480), (580, 514), (598, 665), (665, 735), (744, 675), (742, 417),
        (682, 368), (448, 365), (401, 306), (484, 262), (676, 259), (733, 233), (738, 119), (683, 77), (333, 74), (279, 143), (280, 347), (232, 418), (177, 354), (174, 256)]


class AbstractCar():
    def __init__(self, max_vel, rotation_vel):
        self.max_vel = max_vel
        self.angle = 0
        self.rotation_vel = rotation_vel
        self.img = self.IMG
        self.vel = 0
        self.x, self.y = self.START_POS

        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        if right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)

        offset = (int(self.x - x), int(self.y - y))

        poi = mask.overlap(car_mask, offset)

        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.vel = 0
        self.angle = 0


class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180, 200)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel/2
        self.move()


class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)
        # self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]

        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radiant_angle = math.pi/2
        else:
            desired_radiant_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radiant_angle += math.pi

        difference_in_angel = self.angle - math.degrees(desired_radiant_angle)

        if difference_in_angel >= 180:
            difference_in_angel -= 360

        if difference_in_angel > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angel))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angel))

    def update_path_point(self):
        target = self.path[self.current_point]

        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())

        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return
        self.calculate_angle()
        self.update_path_point()

        super().move()

    def next_level(self, level):
        self.reset()

        self.current_point = self.max_vel + (level - 1) * 0.2
        self.current_point = 0


def draw(win, images, player_car, computer_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    computer_car.draw(win)

    pygame.display.update()


def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()


def handle_collision(player_car, computer_car):
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    computer_finish_poi_collode = computer_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    if computer_finish_poi_collode != None:
        computer_car.reset()
        player_car.reset()

    player_finish_poi_collide = player_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            player_car.reset()


images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
          (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]


player_car = PlayerCar(4, 4)
computer_car = ComputerCar(4, 4, PATH)
run = True

clock = pygame.time.Clock()

FPS = 60


while run:
    clock.tick(FPS)
    draw(WIN, images, player_car, computer_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     pos = pygame.mouse.get_pos()
        #     computer_car.path.append(pos)

    move_player(player_car)
    computer_car.move()
    handle_collision(player_car, computer_car)

print(computer_car.path)
pygame.quit()
