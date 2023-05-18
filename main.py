import random

from settings import *
from player import Player
from enemy import Enemy
from button import Button

pygame.init()


def draw_window(player, sprite_group, walk_or_not, revive_button, store):
    WIN.blit(BACKGROUND, (cam_pos_x, cam_pos_y))

    sprite_group.draw(WIN)

    player.draw(walk_or_not, revive_button)

    store.draw()

    player.info_draw()

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


def player_control(player_pos_x, player_pos_y, keys):
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


def tile_cords(cord_x, cord_y):
    x = int((cord_x - cam_pos_x) / TILE_SIZE)
    y = int((cord_y - cam_pos_y) / TILE_SIZE)
    return x, y


# looking for collision with maps object
def check_map_collision(cord_x, cord_y):
    x, y = tile_cords(cord_x, cord_y)
    return map_array[x, y]


def is_enemy_collision(player, sprites_group):
    for sprite in sprites_group:
        if pygame.sprite.collide_rect(player, sprite):
            player.fight_simulation(sprite)
            if not sprite.is_alive:
                sprites_group.remove(sprite)
            return True
    return False


def heal_zone(player):
    x, y = tile_cords(player.player_pos_x, player.prev_player_pos_y)
    if (x, y) in MAP_HEAL_ZONE:
        player.heal(0.1)


def store_zone(player, store):
    x, y = tile_cords(player.player_pos_x, player.player_pos_y)
    if x == 27 and y == 15:
        store.is_visible = True
    else:
        store.is_visible = False


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

    player = Player("knight")
    sprite_group = pygame.sprite.Group()

    prev_cam_pos_x, prev_cam_pos_y = 0, 0

    revive_button = Button(100, 45, 30, 50, player.revive, "revive button")

    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            mouse_position = pygame.mouse.get_pos()
            player.handle_event(event, mouse_position)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not player.is_alive:
                    revive_button.is_pressed(mouse_position)
        if player.is_alive:
            keys = pygame.key.get_pressed()

            # player control
            player.player_pos_x, player.player_pos_y = player_control(player.player_pos_x, player.player_pos_y, keys)
            player.change_position(player.player_pos_x, player.player_pos_y)

            walk_or_not = player.is_player_moved(cam_pos_x, cam_pos_y, prev_cam_pos_x, prev_cam_pos_y)

            # check collision with enemies
            is_enemy_collision(player, sprite_group)

            # update enemies positions and render new enemy if player kill one of them
            enemy_update(sprite_group, prev_cam_pos_x, prev_cam_pos_y)

            # check if player is in shop zone
            store_zone(player, player.store)

            draw_window(player, sprite_group, walk_or_not, revive_button, player.store)

            # check if player is in heal zone
            heal_zone(player)

            # update previous player position
            player.prev_player_pos_x = player.player_pos_x
            player.prev_player_pos_y = player.player_pos_y

            # update previous camera position
            prev_cam_pos_x, prev_cam_pos_y = cam_pos_x, cam_pos_y
        else:
            draw_window(player, sprite_group, False, revive_button, player.store)

    pygame.quit()


if __name__ == "__main__":
    main()
