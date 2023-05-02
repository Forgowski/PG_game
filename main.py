import random

from settings import *
from character import Character, Enemy
from button import Button

pygame.init()


def draw_window(player, sprite_group, walk_or_not, revive_button):
    WIN.blit(BACKGROUND, (cam_pos_x, cam_pos_y))
    WIN.blit(player.image, (player.rect.x, player.rect.y))
    WIN.blit(hp_text, (0, 10))
    WIN.blit(exp_text, (0, 30))
    pygame.draw.rect(WIN, CLARET, player.hp_background_bar)
    pygame.draw.rect(WIN, RED, player.hp_bar)
    pygame.draw.rect(WIN, GOLD_BACKGROUND, player.exp_background_bar)
    pygame.draw.rect(WIN, GOLD, player.exp_bar)
    if walk_or_not:
        player.update()
    else:
        if player.is_alive:
            player.image = player.images[3]
        else:
            pygame.draw.rect(WIN, BLACK, revive_button.rectangle)
            WIN.blit(revive_button.rectangle_text, revive_button.rectangle_text_position)
            player.death_animation()
    sprite_group.draw(WIN)
    pygame.display.update()


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
    return map_array[x, y]


# this will check if we need walk animation
def is_player_moved(player_pos_x, player_pos_y, prev_player_pos_x, prev_player_pos_y, prev_cam_pos_x, prev_cam_pos_y):
    return player_pos_x != prev_player_pos_x or player_pos_y != prev_player_pos_y or cam_pos_x != prev_cam_pos_x or \
        cam_pos_y != prev_cam_pos_y


def is_enemy_collision(player, sprites_group):
    for sprite in sprites_group:
        if pygame.sprite.collide_rect(player, sprite):
            sprites_group.remove(sprite)
            if player.update_hp_bar(sprite.attack_power):
                pass
            player.update_exp_bar(sprite.exp_drop)
            return True
    return False


def draw_fight_scene():
    pass


def enemy_update(sprite_group, prev_cam_pos_x, prev_cam_pos_y):
    while len(sprite_group) < OPPONENTS_NUMBER:
        enemy = Enemy()
        x, y = random.randint(0 + cam_pos_x, BACKGROUND_X - 200 + cam_pos_x), \
            random.randint(0 + cam_pos_y, BACKGROUND_Y - 200 + cam_pos_y)

        while check_map_collision(x, y):
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

    player_pos_x, player_pos_y = 50, 50

    prev_player_pos_x, prev_player_pos_y = 0, 0

    prev_cam_pos_x, prev_cam_pos_y = 0, 0

    revive_button = Button(100, 45, 30, 50, player.revive, "revive button")

    text_position_x = (revive_button.rectangle.width - (
        revive_button.rectangle_text.get_width())) / 2 + revive_button.rectangle.x

    text_position_y = (revive_button.rectangle.height - (
        revive_button.rectangle_text.get_height())) / 2 + revive_button.rectangle.y

    revive_button.rectangle_text_position = (text_position_x, text_position_y)

    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                revive_button.is_pressed(mouse_position)
        if player.is_alive:
            player_pos_x, player_pos_y = player_moves(player_pos_x, player_pos_y)
            player.change_position(player_pos_x, player_pos_y)

            walk_or_not = is_player_moved(player_pos_x, player_pos_y, prev_player_pos_x, prev_player_pos_y,
                                          prev_cam_pos_x, prev_cam_pos_y)

            enemy_update(sprite_group, prev_cam_pos_x, prev_cam_pos_y)

            draw_window(player, sprite_group, walk_or_not, revive_button)

            is_enemy_collision(player, sprite_group)
            prev_player_pos_x, prev_player_pos_y = player_pos_x, player_pos_y
            prev_cam_pos_x, prev_cam_pos_y = cam_pos_x, cam_pos_y
        else:
            draw_window(player, sprite_group, False, revive_button)

    pygame.quit()


if __name__ == "__main__":
    main()
