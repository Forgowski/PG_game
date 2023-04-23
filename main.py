from settings import *
from character import Character

pygame.init()


def draw_window():
    WIN.blit(BACKGROUND, (cam_pos_x, cam_pos_y))
    pygame.display.update()


def camera_moves(direction):
    global cam_pos_y
    global cam_pos_x
    if direction == "up" and cam_pos_y + CAM_SPEED <= 0:
        cam_pos_y += CAM_SPEED

    if direction == "down" and cam_pos_y - CAM_SPEED - HEIGHT >= -BACKGROUND_SIZE[1]:
        cam_pos_y -= CAM_SPEED

    if direction == "right" and cam_pos_x - CAM_SPEED - WIDTH >= -BACKGROUND_SIZE[0]:
        cam_pos_x -= CAM_SPEED

    if direction == "left" and cam_pos_x + CAM_SPEED <= 0:
        cam_pos_x += CAM_SPEED


def player_moves(player_pos_x, player_pos_y):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_pos_y - CAM_SPEED >= 0:
        player_pos_y -= CAM_SPEED

    if player_pos_y < CAM_MARGIN and keys[pygame.K_UP]:
        camera_moves("up")

    if keys[pygame.K_DOWN] and player_pos_y + CAM_SPEED + CHARACTER_HEIGHT <= HEIGHT:
        player_pos_y += CAM_SPEED

    if player_pos_y > HEIGHT - CAM_MARGIN and keys[pygame.K_DOWN]:
        camera_moves("down")

    if keys[pygame.K_RIGHT] and player_pos_x + CAM_SPEED + CHARACTER_WIDTH <= WIDTH:
        player_pos_x += CAM_SPEED

    if player_pos_x > WIDTH - CAM_MARGIN and keys[pygame.K_RIGHT]:
        camera_moves("right")

    if keys[pygame.K_LEFT] and player_pos_x - CAM_SPEED >= 0:
        player_pos_x -= CAM_SPEED

    if player_pos_x < CAM_MARGIN and keys[pygame.K_LEFT]:
        camera_moves("left")

    return player_pos_x, player_pos_y


def main():
    clock = pygame.time.Clock()
    run = True

    player = Character("knight")
    sprite_group = pygame.sprite.Group()
    sprite_group.add(player)

    player_pos_x = 0
    player_pos_y = 0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #
        sprite_group.update()

        player_pos_x, player_pos_y = player_moves(player_pos_x, player_pos_y)
        player.change_position(player_pos_x, player_pos_y)

        draw_window()
        sprite_group.draw(WIN)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
