import pygame
import pygame_menu

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
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #
        camera_moves()
        print(f'{cam_pos_x} +" " +{cam_pos_y}')
        draw_window()

    pygame.quit()


if __name__ == "__main__":
    main()
