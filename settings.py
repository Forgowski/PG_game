import pygame

WIDTH, HEIGHT, = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
FPS = 60

BACKGROUND_SIZE = (3000, 2000)
background = pygame.image.load("assets/map/map.png").convert()
BACKGROUND = pygame.transform.scale(background, BACKGROUND_SIZE)

CHARACTER_HEIGHT = 30
CHARACTER_WIDTH = 20

CAM_MARGIN = 60
CAM_SPEED = 10
cam_pos_x = 0
cam_pos_y = 0
