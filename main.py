import random

from settings import *
from character import Character, Enemy

pygame.init()


def camera_moves(direction):
    global cam_pos_x, cam_pos_y

    if direction == "up" and cam_pos_y + CAM_SPEED <= 0:
        cam_pos_y += CAM_SPEED

    if direction == "down" and cam_pos_y - CAM_SPEED - HEIGHT >= -BACKGROUND_SIZE[1]:
        cam_pos_y -= CAM_SPEED

    if direction == "right" and cam_pos_x - CAM_SPEED - WIDTH >= -BACKGROUND_SIZE[0]:
        cam_pos_x -= CAM_SPEED

    if direction == "left" and cam_pos_x + CAM_SPEED <= 0:
        cam_pos_x += CAM_SPEED


def draw_window(player, sprite_group, walk_or_not):
    if walk_or_not:
        player.update()
    else:
        player.image = player.images[3]

    WIN.blit(BACKGROUND, (cam_pos_x, cam_pos_y))
    WIN.blit(player.image, (player.rect.x, player.rect.y))
    sprite_group.draw(WIN)
    pygame.display.update()


def player_moves(player_pos_x, player_pos_y):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_pos_y - CAM_SPEED >= 0:
        if not check_map_collision(player_pos_x, player_pos_y - CAM_SPEED, "player"):
            player_pos_y -= CAM_SPEED

    if player_pos_y < CAM_MARGIN and keys[pygame.K_UP]:
        if not check_map_collision(player_pos_x, player_pos_y - CAM_SPEED, "player"):
            camera_moves("up")

    if keys[pygame.K_DOWN] and player_pos_y + CAM_SPEED + CHARACTER_HEIGHT <= HEIGHT:
        if not check_map_collision(player_pos_x, player_pos_y + CAM_SPEED, "player"):
            player_pos_y += CAM_SPEED

    if player_pos_y > HEIGHT - CAM_MARGIN and keys[pygame.K_DOWN]:
        if not check_map_collision(player_pos_x, player_pos_y + CAM_SPEED, "player"):
            camera_moves("down")

    if keys[pygame.K_RIGHT] and player_pos_x + CAM_SPEED + CHARACTER_WIDTH <= WIDTH:
        if not check_map_collision(player_pos_x + CAM_SPEED, player_pos_y, "player"):
            player_pos_x += CAM_SPEED

    if player_pos_x > WIDTH - CAM_MARGIN and keys[pygame.K_RIGHT]:
        if not check_map_collision(player_pos_x + CAM_SPEED, player_pos_y, "player"):
            camera_moves("right")

    if keys[pygame.K_LEFT] and player_pos_x - CAM_SPEED >= 0:
        if not check_map_collision(player_pos_x - CAM_SPEED, player_pos_y, "player"):
            player_pos_x -= CAM_SPEED

    if player_pos_x < CAM_MARGIN and keys[pygame.K_LEFT]:
        if not check_map_collision(player_pos_x - CAM_SPEED, player_pos_y, "player"):
            camera_moves("left")

    return player_pos_x, player_pos_y


# looking for collision with maps object
def check_map_collision(player_pos_x, player_pos_y, sprite_type):
    if sprite_type == "player":
        x = int((player_pos_x - cam_pos_x) / TILE_SIZE)
        y = int((player_pos_y - cam_pos_y) / TILE_SIZE)
    else:
        x = int((player_pos_x - cam_pos_x) / TILE_SIZE)
        y = int((player_pos_y - cam_pos_y) / TILE_SIZE)
    return map_array[x, y]


# this will check if we need walk animation
def is_player_moved(player_pos_x, player_pos_y, prev_player_pos_x, prev_player_pos_y, prev_cam_pos_x, prev_cam_pos_y):
    return player_pos_x != prev_player_pos_x or player_pos_y != prev_player_pos_y or cam_pos_x != prev_cam_pos_x or \
        cam_pos_y != prev_cam_pos_y


def is_enemy_collision(player, sprites_group):
    for sprite in sprites_group:
        if pygame.sprite.collide_rect(player, sprite):
            sprites_group.remove(sprite)
            return True
    return False


def draw_fight_scene():
    pass


def enemy_update(sprite_group, prev_cam_pos_x, prev_cam_pos_y):
    while len(sprite_group) < OPPONENTS_NUMBER:
        enemy = Enemy()
        x, y = random.randint(0 + cam_pos_x, BACKGROUND_X - 200 + cam_pos_x), \
            random.randint(0 + cam_pos_y, BACKGROUND_Y - 200 + cam_pos_y)

        while check_map_collision(x, y, "enemy"):
            x, y = random.randint(0 + cam_pos_x, BACKGROUND_X - 200 + cam_pos_x), \
                random.randint(0 + cam_pos_y, BACKGROUND_Y - 200 + cam_pos_y)

        enemy.change_position(x, y)
        sprite_group.add(enemy)

    if cam_pos_x != prev_cam_pos_x or cam_pos_y != prev_cam_pos_y:
        for sprite in sprite_group:
            sprite.change_position(sprite.rect.x + cam_pos_x - prev_cam_pos_x,
                                   sprite.rect.y + cam_pos_y - prev_cam_pos_y)


def main():
    clock = pygame.time.Clock()
    run = True

    player = Character("knight")
    sprite_group = pygame.sprite.Group()

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

        walk_or_not = is_player_moved(player_pos_x, player_pos_y, prev_player_pos_x, prev_player_pos_y, prev_cam_pos_x,
                                      prev_cam_pos_y)

        enemy_update(sprite_group, prev_cam_pos_x, prev_cam_pos_y)

        draw_window(player, sprite_group, walk_or_not)

        is_enemy_collision(player, sprite_group)
        print(cam_pos_x, cam_pos_y)
        prev_player_pos_x, prev_player_pos_y = player_pos_x, player_pos_y
        prev_cam_pos_x, prev_cam_pos_y = cam_pos_x, cam_pos_y

    pygame.quit()


if __name__ == "__main__":
    main()
