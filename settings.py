import pygame
import numpy as np
from pygame import font

WIDTH, HEIGHT, = 1800, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
FPS = 60

BACKGROUND_X = 3000
BACKGROUND_Y = BACKGROUND_X * 2 / 3
BACKGROUND_SIZE = (BACKGROUND_X, BACKGROUND_Y)
background = pygame.image.load("assets/map/map.png").convert()
BACKGROUND = pygame.transform.scale(background, BACKGROUND_SIZE)
BUTTON_PNG = pygame.transform.scale(pygame.image.load("assets/player/gui/button.png"), (100, 25))

RED = (255, 0, 0)
CLARET = (150, 0, 100)
GOLD = (244, 168, 13)
GOLD_BACKGROUND = (105, 79, 7)
BLACK = (0, 0, 0)
BROWN = (77, 41, 4)

ITEMS_WIDTH = 32
ITEMS_HEIGHT = 32

TILE_SIZE = BACKGROUND_X / 60

OPPONENTS_NUMBER = 15

CHARACTER_HEIGHT = 30
CHARACTER_WIDTH = 20

CAM_MARGIN = 60
CAM_SPEED = 10
cam_pos_x = 0
cam_pos_y = 0

pygame.font.init()
stats_font = font.SysFont('georgia', 18)
my_font = font.SysFont('Arial', 15)
my_bold_font = font.SysFont('Arial', 15, bold=True)

hp_text = my_font.render('HP', True, (255, 255, 255))
exp_text = my_font.render('EXP', True, (255, 255, 255))

map_array = np.zeros((60, 40), dtype=int)
np.set_printoptions(threshold=np.inf)

MAP_HEAL_ZONE = []
MAP_COLLISION_CORDS = [
    [24, 32, 0, 15],
    [0, 10, 21, 22],
    [0, 1, 34, 40],
    [0, 7, 39, 40],
    [6, 7, 34, 40],
    [15, 22, 28, 32],
    [29, 31, 32, 40],
    [33, 34, 33, 40],
    [43, 60, 29, 32],
    [3, 4, 35, 38]
]


def setting_loops():
    for each in MAP_COLLISION_CORDS:
        for i in range(each[0], each[1]):
            for j in range(each[2], each[3]):
                map_array[i][j] = 1

    for i in range(1, 6):
        for j in range(34, 39):
            MAP_HEAL_ZONE.append((i, j))


setting_loops()
