import random

from boss import Boss
from settings import *
from player import Player
from enemy import Enemy
from button import Button
from sound import Sounds
from fight import Fight
from menu import Menu
from save import save_game

pygame.init()


def draw_window(player, sprite_group, walk_or_not, revive_button, store, sound, cam_pos_x, cam_pos_y, boss):
    WIN.blit(BACKGROUND, (cam_pos_x, cam_pos_y))

    sprite_group.draw(WIN)

    player.draw(walk_or_not, revive_button)

    boss.draw()

    store.draw()

    player.info_draw()

    sound.draw()

    pygame.display.update()


def camera_moves(direction, cam_pos_x, cam_pos_y):
    if direction == "up" and cam_pos_y + CAM_SPEED <= 0:
        cam_pos_y += CAM_SPEED

    if direction == "down" and cam_pos_y - CAM_SPEED - HEIGHT >= -BACKGROUND_SIZE[1]:
        cam_pos_y -= CAM_SPEED

    if direction == "right" and cam_pos_x - CAM_SPEED - WIDTH >= -BACKGROUND_SIZE[0]:
        cam_pos_x -= CAM_SPEED

    if direction == "left" and cam_pos_x + CAM_SPEED <= 0:
        cam_pos_x += CAM_SPEED

    return cam_pos_x, cam_pos_y


def player_control(player_pos_x, player_pos_y, keys, cam_pos_x, cam_pos_y):
    if keys[pygame.K_UP] and player_pos_y - CAM_SPEED >= 0:
        if not check_map_collision(player_pos_x, player_pos_y - CAM_SPEED, cam_pos_x, cam_pos_y):
            player_pos_y -= CAM_SPEED

    if player_pos_y < CAM_MARGIN and keys[pygame.K_UP]:
        if not check_map_collision(player_pos_x, player_pos_y - CAM_SPEED, cam_pos_x, cam_pos_y):
            cam_pos_x, cam_pos_y = camera_moves("up", cam_pos_x, cam_pos_y)

    if keys[pygame.K_DOWN] and player_pos_y + CAM_SPEED + CHARACTER_HEIGHT <= HEIGHT:
        if not check_map_collision(player_pos_x, player_pos_y + CAM_SPEED, cam_pos_x, cam_pos_y):
            player_pos_y += CAM_SPEED

    if player_pos_y > HEIGHT - CAM_MARGIN and keys[pygame.K_DOWN]:
        if not check_map_collision(player_pos_x, player_pos_y + CAM_SPEED, cam_pos_x, cam_pos_y):
            cam_pos_x, cam_pos_y = camera_moves("down", cam_pos_x, cam_pos_y)

    if keys[pygame.K_RIGHT] and player_pos_x + CAM_SPEED + CHARACTER_WIDTH <= WIDTH:
        if not check_map_collision(player_pos_x + CAM_SPEED, player_pos_y, cam_pos_x, cam_pos_y):
            player_pos_x += CAM_SPEED

    if player_pos_x > WIDTH - CAM_MARGIN and keys[pygame.K_RIGHT]:
        if not check_map_collision(player_pos_x + CAM_SPEED, player_pos_y, cam_pos_x, cam_pos_y):
            cam_pos_x, cam_pos_y = camera_moves("right", cam_pos_x, cam_pos_y)

    if keys[pygame.K_LEFT] and player_pos_x - CAM_SPEED >= 0:
        if not check_map_collision(player_pos_x - CAM_SPEED, player_pos_y, cam_pos_x, cam_pos_y):
            player_pos_x -= CAM_SPEED

    if player_pos_x < CAM_MARGIN and keys[pygame.K_LEFT]:
        if not check_map_collision(player_pos_x - CAM_SPEED, player_pos_y, cam_pos_x, cam_pos_y):
            cam_pos_x, cam_pos_y = camera_moves("left", cam_pos_x, cam_pos_y)

    return player_pos_x, player_pos_y, cam_pos_x, cam_pos_y


def tile_cords(cord_x, cord_y, cam_pos_x, cam_pos_y):
    x = int((cord_x - cam_pos_x) / TILE_SIZE)
    y = int((cord_y - cam_pos_y) / TILE_SIZE)
    return x, y


# looking for collision with maps object
def check_map_collision(cord_x, cord_y, cam_pos_x, cam_pos_y):
    x, y = tile_cords(cord_x, cord_y, cam_pos_x, cam_pos_y)
    return map_array[x, y]


def is_enemy_collision(player, sprites_group):
    for sprite in sprites_group:
        if pygame.sprite.collide_rect(player, sprite):
            if not player.is_simulation_active:
                Fight(player, sprite)
            else:
                player.fight_simulation(sprite)
            if not sprite.is_alive:
                sprites_group.remove(sprite)
            return True
    return False


def heal_zone(player, cam_pos_x, cam_pos_y):
    x, y = tile_cords(player.player_pos_x, player.prev_player_pos_y, cam_pos_x, cam_pos_y)
    if (x, y) in MAP_HEAL_ZONE:
        player.heal(0.1)


def store_zone(player, cam_pos_x, cam_pos_y):
    x, y = tile_cords(player.player_pos_x, player.player_pos_y, cam_pos_x, cam_pos_y)
    if x == 27 and y == 15:
        player.store.is_visible = True
    else:
        player.store.is_visible = False


def draw_fight_scene():
    pass


def enemy_update(sprite_group, prev_cam_pos_x, prev_cam_pos_y, opponents_lvl, cam_pos_x, cam_pos_y, boss):
    while len(sprite_group) < OPPONENTS_NUMBER:
        enemy = Enemy(opponents_lvl)
        x, y = random.randint(0 + cam_pos_x, BACKGROUND_X - 200 + cam_pos_x), \
            random.randint(0 + cam_pos_y, BACKGROUND_Y - 200 + cam_pos_y)

        while check_map_collision(x, y, cam_pos_x, cam_pos_y):
            x, y = random.randint(0 + cam_pos_x, BACKGROUND_X - 200 + cam_pos_x), \
                random.randint(0 + cam_pos_y, BACKGROUND_Y - 200 + cam_pos_y)

        enemy.change_position(x, y)
        sprite_group.add(enemy)

    if cam_pos_x != prev_cam_pos_x or cam_pos_y != prev_cam_pos_y:
        for sprite in sprite_group:
            sprite.change_position(sprite.rect.x + cam_pos_x - prev_cam_pos_x,
                                   sprite.rect.y + cam_pos_y - prev_cam_pos_y)
        boss.change_position(boss.rect.x + cam_pos_x - prev_cam_pos_x,
                             boss.rect.y + cam_pos_y - prev_cam_pos_y)


def main():
    clock = pygame.time.Clock()

    sprite_group = pygame.sprite.Group()
    sound = Sounds()

    cam_pos_x, cam_pos_y = 0, 0
    prev_cam_pos_x, prev_cam_pos_y = 0, 0

    menu = Menu()
    is_loaded, player = menu.main_loop()

    if is_loaded == 0:
        player = Player("knight")
        boss = Boss(1)

    revive_button = Button(100, 25, 30, 50, player.revive, "revive button", BUTTON_PNG)

    run = True
    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            mouse_position = pygame.mouse.get_pos()
            player.handle_event(event, mouse_position, sprite_group)
            sound.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not player.is_alive:
                    revive_button.is_pressed(mouse_position)
        if player.is_alive:
            keys = pygame.key.get_pressed()

            # player control
            player.player_pos_x, player.player_pos_y, cam_pos_x, cam_pos_y = player_control(player.player_pos_x,
                                                                                            player.player_pos_y, keys,
                                                                                            cam_pos_x, cam_pos_y)
            player.change_position(player.player_pos_x, player.player_pos_y)

            # check if player moved
            walk_or_not = player.is_player_moved(cam_pos_x, cam_pos_y, prev_cam_pos_x, prev_cam_pos_y)

            # check collision with enemies
            is_enemy_collision(player, sprite_group)

            # update enemies positions and render new enemy if player kill one of them
            enemy_update(sprite_group, prev_cam_pos_x, prev_cam_pos_y, player.opponents_level, cam_pos_x, cam_pos_y,
                         boss)

            # check if player is in shop zone
            store_zone(player, cam_pos_x, cam_pos_y)

            draw_window(player, sprite_group, walk_or_not, revive_button, player.store, sound, cam_pos_x, cam_pos_y,
                        boss)

            # check if player is in heal zone
            heal_zone(player, cam_pos_x, cam_pos_y)

            # update previous player position
            player.prev_player_pos_x = player.player_pos_x
            player.prev_player_pos_y = player.player_pos_y

            # update previous camera position
            prev_cam_pos_x, prev_cam_pos_y = cam_pos_x, cam_pos_y
        else:
            draw_window(player, sprite_group, False, revive_button, player.store, sound, cam_pos_x, cam_pos_y, boss)

    save_game(player, boss)
    pygame.quit()


if __name__ == "__main__":
    main()
