import pygame
import numpy as np

WIDTH, HEIGHT, = 1800, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
FPS = 60

BACKGROUND_X = 3000
BACKGROUND_Y = BACKGROUND_X * 2 / 3
BACKGROUND_SIZE = (BACKGROUND_X, BACKGROUND_Y)
background = pygame.image.load("assets/map/map.png").convert()
BACKGROUND = pygame.transform.scale(background, BACKGROUND_SIZE)

RED = (255, 0, 0)
CLARET = (150, 0, 100)
GOLD = (244, 168, 13)
GOLD_BACKGROUND = (105, 79, 7)

TILE_SIZE = BACKGROUND_X / 60

OPPONENTS_NUMBER = 15
opponents_level = 1

CHARACTER_HEIGHT = 30
CHARACTER_WIDTH = 20

CAM_MARGIN = 60
CAM_SPEED = 10
cam_pos_x = 0
cam_pos_y = 0

map_array = np.zeros((60, 40), dtype=int)
np.set_printoptions(threshold=np.inf)
for i in range(24, 31):
    for j in range(15):
        map_array[i][j] = 1
