import pygame
from character import Character

WIDTH, HEIGHT, = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
FPS = 60

BACKGROUND_SIZE = (3000, 2000)
background = pygame.image.load("assets/map/map.png").convert()
BACKGROUND = pygame.transform.scale(background, BACKGROUND_SIZE)

CAM_SPEED = 20
cam_pos_x = 0
cam_pos_y = 0

player_pos_x = 0
player_pos_y = 0

pygame.init()


def draw_window():
    WIN.blit(BACKGROUND, (cam_pos_x, cam_pos_y))
    pygame.display.update()


def camera_moves():
    global cam_pos_y
    global cam_pos_x
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and cam_pos_y + CAM_SPEED <= 0:
        cam_pos_y += CAM_SPEED
    if keys[pygame.K_DOWN] and cam_pos_y - CAM_SPEED - HEIGHT >= -BACKGROUND_SIZE[1]:
        cam_pos_y -= CAM_SPEED
    if keys[pygame.K_RIGHT] and cam_pos_x - CAM_SPEED - WIDTH >= -BACKGROUND_SIZE[0]:
        cam_pos_x -= CAM_SPEED
    if keys[pygame.K_LEFT] and cam_pos_x + CAM_SPEED <= 0:
        cam_pos_x += CAM_SPEED


def main():
    clock = pygame.time.Clock()
    run = True
    player = Character("knight")
    sprite_group = pygame.sprite.Group()
    sprite_group.add(player)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #
        sprite_group.update()
        camera_moves()
        draw_window()
        sprite_group.draw(WIN)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
