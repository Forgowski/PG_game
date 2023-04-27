from settings import *
from character import Character

pygame.init()


def draw_window(sprite_group, walk_or_not):
    if walk_or_not:
        sprite_group.update()
    else:
        sprite_group.sprites()[0].image = sprite_group.sprites()[0].images[0]
    WIN.blit(BACKGROUND, (cam_pos_x, cam_pos_y))
    sprite_group.draw(WIN)
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
        if not check_map_collision(player_pos_x, player_pos_y - CAM_SPEED):
            player_pos_y -= CAM_SPEED

    if player_pos_y < CAM_MARGIN and keys[pygame.K_UP]:
        if not check_map_collision(player_pos_x, player_pos_y - CAM_SPEED):
            camera_moves("up")

    if keys[pygame.K_DOWN] and player_pos_y + CAM_SPEED + CHARACTER_HEIGHT <= HEIGHT:
        if not check_map_collision(player_pos_x, player_pos_y + CAM_SPEED):
            player_pos_y += CAM_SPEED

    if player_pos_y > HEIGHT - CAM_MARGIN and keys[pygame.K_DOWN]:
        if not check_map_collision(player_pos_x, player_pos_y + CAM_SPEED):
            camera_moves("down")

    if keys[pygame.K_RIGHT] and player_pos_x + CAM_SPEED + CHARACTER_WIDTH <= WIDTH:
        if not check_map_collision(player_pos_x + CAM_SPEED, player_pos_y):
            player_pos_x += CAM_SPEED

    if player_pos_x > WIDTH - CAM_MARGIN and keys[pygame.K_RIGHT]:
        if not check_map_collision(player_pos_x + CAM_SPEED, player_pos_y):
            camera_moves("right")

    if keys[pygame.K_LEFT] and player_pos_x - CAM_SPEED >= 0:
        if not check_map_collision(player_pos_x - CAM_SPEED, player_pos_y):
            player_pos_x -= CAM_SPEED

    if player_pos_x < CAM_MARGIN and keys[pygame.K_LEFT]:
        if not check_map_collision(player_pos_x - CAM_SPEED, player_pos_y):
            camera_moves("left")

    return player_pos_x, player_pos_y


# looking for collision with maps object
def check_map_collision(player_pos_x, player_pos_y):
    x = int((player_pos_x - cam_pos_x) / TILE_SIZE)
    y = int((player_pos_y - cam_pos_y) / TILE_SIZE)
    if map_array[x, y]:
        return True


# this will check if we need walk animation
def is_player_moved(player_pos_x, player_pos_y, prev_player_pos_x, prev_player_pos_y, cam_pos_x,
                    cam_pos_y, prev_cam_pos_x, prev_cam_pos_y):
    return player_pos_x != prev_player_pos_x or player_pos_y != prev_player_pos_y or cam_pos_x != prev_cam_pos_x or \
        cam_pos_y != prev_cam_pos_y


def main():
    clock = pygame.time.Clock()
    run = True

    player = Character("knight")
    sprite_group = pygame.sprite.Group()
    sprite_group.add(player)

    player_pos_x, player_pos_y = 0, 0

    prev_player_pos_x, prev_player_pos_y = 0, 0

    prev_cam_pos_x, prev_cam_pos_y = 0, 0

    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        player_pos_x, player_pos_y = player_moves(player_pos_x, player_pos_y)
        player.change_position(player_pos_x, player_pos_y)

        walk_or_not = is_player_moved(player_pos_x, player_pos_y, prev_player_pos_x, prev_player_pos_y, cam_pos_x,
                                      cam_pos_y, prev_cam_pos_x, prev_cam_pos_y)
        draw_window(sprite_group, walk_or_not)

        prev_player_pos_x, prev_player_pos_y = player_pos_x, player_pos_y
        prev_cam_pos_x, prev_cam_pos_y = cam_pos_x, cam_pos_y

    pygame.quit()


if __name__ == "__main__":
    main()
