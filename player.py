import random
from equipment import *
from stats import Stats
from button import Button

knight = [pygame.image.load("assets/player/knight/knight.png"),
          pygame.image.load("assets/player/knight/knight2.png"),
          pygame.image.load("assets/player/knight/knight3.png"),
          pygame.image.load("assets/player/knight/knight4.png"),
          pygame.image.load("assets/player/knight/knight5.png"),
          ]

wizard = [pygame.image.load("assets/player/wizard/wizard.png"),
          pygame.image.load("assets/player/wizard/wizard2.png"),
          pygame.image.load("assets/player/wizard/wizard3.png"),
          pygame.image.load("assets/player/wizard/wizard4.png"),
          pygame.image.load("assets/player/wizard/wizard5.png"),
          ]

knight_death = [pygame.image.load("assets/player/knight/knight_d.png"),
                pygame.image.load("assets/player/knight/knight_d1.png"),
                pygame.image.load("assets/player/knight/knight_d2.png"),
                pygame.image.load("assets/player/knight/knight_d3.png"),
                ]

wizard_death = [pygame.image.load("assets/player/wizard/wizard_d.png"),
                pygame.image.load("assets/player/wizard/wizard_d1.png"),
                pygame.image.load("assets/player/wizard/wizard_d2.png"),
                pygame.image.load("assets/player/wizard/wizard_d3.png"),
                ]

active_png = pygame.transform.scale(pygame.image.load("assets/player/gui/active.png"), (15, 15))
check_box_png = pygame.transform.scale(pygame.image.load("assets/player/gui/box.png"), (25, 25))


class Player(pygame.sprite.Sprite):
    def __init__(self, hero_type):
        super().__init__()
        if hero_type == "knight":
            self.images = knight
            self.death_images = knight_death
        else:
            self.images = wizard
            self.death_images = wizard_death

        self.hero_type = hero_type
        self.store = Store(self.hero_type)

        self.player_pos_x, self.player_pos_y = 50, 50

        self.prev_player_pos_x, self.prev_player_pos_y = 50, 50

        self.is_alive = True
        self.lvl = 1

        self.stats = Stats(100, 50, 0, 0)
        self.hp = 100
        self.exp = 0
        self.opponents_level = 1

        self.hp_bar = pygame.Rect(30, 10, 100, 15)
        self.hp_background_bar = pygame.Rect(30, 10, 100, 15)
        self.exp_to_next_level = 100
        self.exp_bar = pygame.Rect(30, 30, 0, 15)
        self.exp_background_bar = pygame.Rect(30, 30, 100, 15)
        self.info_rectangle = None
        self.is_info_rectangle_visible = False
        self.info_text = None

        self.simulation_button = Button(25, 25, 10, HEIGHT - 70, self.turn_on_off_simulation, None, check_box_png)
        self.is_simulation_active = True
        self.simulation_text = my_bold_font.render('fight simulation', True, (0, 0, 0))

        self.current_image = 0
        self.current_death_image = 0
        self.image = self.images[self.current_image]

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.make_slower = 6
        self.counter = 1
        self.death_frame_counter = 1

        self.equipment = Equipment()

    def update(self):
        if self.counter % self.make_slower == 0:
            self.current_image += 1
            if self.current_image >= len(self.images):
                self.current_image = 0
            self.image = self.images[self.current_image]
            self.counter = 1
        self.counter += 1

    def change_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def is_player_moved(self, cam_pos_x, cam_pos_y, prev_cam_pos_x, prev_cam_pos_y):
        return self.player_pos_x != self.prev_player_pos_x or self.player_pos_y != self.prev_player_pos_y or \
            cam_pos_x != prev_cam_pos_x or cam_pos_y != prev_cam_pos_y

    def update_hp(self, value):
        if self.hp - value <= 0:
            self.hp -= value
            self.is_alive = False
            return True

        self.hp -= value

    def update_hp_bar(self):
        self.hp_bar.width = self.hp / self.stats.max_hp * 100

    def update_exp_bar(self, value):
        self.exp += value
        while self.exp >= self.exp_to_next_level:
            self.stats.upgrade_points += 4
            self.stats.level_up()
            self.lvl += 1
            self.exp -= self.exp_to_next_level
            self.exp_to_next_level *= 2

    def death_animation(self):
        if self.death_frame_counter % self.make_slower == 0:
            self.image = self.death_images[self.current_death_image]
            if self.current_death_image < len(self.death_images) - 1:
                self.current_death_image += 1

        self.death_frame_counter += 1

    def revive(self):
        self.is_alive = True
        self.hp = 1
        self.update_hp(0)
        self.death_frame_counter = 1
        self.current_death_image = 0

    def draw(self, walk_or_not, revive_button):
        self.exp_bar.width = int(self.exp / self.exp_to_next_level * 100)
        self.update_hp_bar()
        WIN.blit(self.image, (self.rect.x, self.rect.y))
        WIN.blit(hp_text, (0, 10))
        WIN.blit(exp_text, (0, 30))
        pygame.draw.rect(WIN, CLARET, self.hp_background_bar)
        pygame.draw.rect(WIN, RED, self.hp_bar)
        pygame.draw.rect(WIN, GOLD_BACKGROUND, self.exp_background_bar)
        pygame.draw.rect(WIN, GOLD, self.exp_bar)
        if walk_or_not:
            self.update()

        else:
            if self.is_alive:
                self.image = self.images[3]

            else:
                revive_button.draw()
                self.death_animation()

        if self.equipment.is_visible:
            self.equipment.draw()

        if self.stats.is_visible:
            self.stats.draw()

        WIN.blit(self.simulation_button.image, self.simulation_button.rectangle.topleft)
        WIN.blit(self.simulation_text,
                 (self.simulation_button.rectangle.topright[0] + 5, self.simulation_button.rectangle.topright[1] + 3))

        if self.is_simulation_active:
            WIN.blit(active_png,
                     (self.simulation_button.rectangle.topleft[0] + 5, self.simulation_button.rectangle.topleft[1] + 5))

    def info_draw(self):
        if self.is_info_rectangle_visible and (self.store.is_visible or self.equipment.is_visible):
            pygame.draw.rect(WIN, BLACK, self.info_rectangle)
            WIN.blit(self.info_text, self.info_rectangle.topleft)

    def fight_simulation(self, enemy_object):
        while self.is_alive and enemy_object.is_alive:
            if random.randint(1, 100) > enemy_object.stats.agility:
                enemy_object.update_hp(self.stats.attack_power)

                if random.randint(1, 100) < self.stats.critical_damage_chance:
                    enemy_object.update_hp(self.stats.attack_power)

            if enemy_object.is_alive:
                if random.randint(1, 100) > self.stats.agility:
                    self.update_hp(enemy_object.stats.attack_power)

                    if random.randint(1, 100) > self.stats.critical_damage_chance:
                        self.update_hp(enemy_object.stats.attack_power)

                if not self.is_alive:
                    enemy_object.heal()
            else:
                self.update_exp_bar(enemy_object.exp_drop)
                self.equipment.add_gold(enemy_object.gold_drop)

    def turn_on_off_simulation(self):
        if self.is_simulation_active:
            self.is_simulation_active = False
        else:
            self.is_simulation_active = True

    def heal(self, value):
        if self.hp == self.stats.max_hp:
            return 0
        else:
            if self.hp + value > self.stats.max_hp:
                self.hp = self.stats.max_hp
            else:
                self.hp = self.hp + value
        return 1

    def handle_event(self, event, mouse_position, enemies):
        # open equipment
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if self.equipment.is_visible:
                    self.equipment.is_visible = False
                else:
                    self.equipment.is_visible = True
                    self.stats.is_visible = False

            # open stats
            if event.key == pygame.K_s:
                if self.stats.is_visible:
                    self.stats.is_visible = False
                else:
                    self.stats.is_visible = True
                    self.equipment.is_visible = False

        # check that player want to buy item
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_RIGHT and self.store.is_visible:

                for i in self.store.available_items:

                    if i.rectangle.collidepoint(mouse_position):

                        if self.equipment.gold >= i.price:

                            if i.name == "level_up":
                                for each in enemies:
                                    each.level_up()
                                self.equipment.subtract_gold(i.price)
                                self.opponents_level += 1

                            elif self.equipment.add_item(create_item(i.name)):
                                self.stats.attack_power += i.attack_power

            # check that player want to use some item
            if event.button == pygame.BUTTON_RIGHT and self.equipment.is_visible:
                for i in self.equipment.items:
                    if i.rectangle.collidepoint(mouse_position) and i.use is not None:
                        if i.use(self):
                            self.equipment.item_used(i)

            # check that player want sell some item
            if event.button == pygame.BUTTON_LEFT and self.equipment.is_visible and self.store.is_visible:
                for i in self.equipment.items:
                    if i.rectangle.collidepoint(mouse_position):
                        print(i.name)
                        self.equipment.sell_item(i)
                        self.stats.attack_power -= i.attack_power

            # upgrade stats
            if event.button == pygame.BUTTON_LEFT and self.stats.is_visible:
                self.stats.event_handle(mouse_position)

            if event.button == pygame.BUTTON_LEFT:
                self.simulation_button.is_pressed(mouse_position)

        # Show info box for store items
        if self.store.is_visible:
            for i in self.store.available_items:
                if i.rectangle.collidepoint(mouse_position):
                    i.info_rectangle.bottomright = mouse_position
                    self.info_rectangle = i.info_rectangle
                    self.info_text = i.info_text
                    self.is_info_rectangle_visible = True
                    return True

        # Show info box for equipment items
        if self.equipment.is_visible:
            for i in self.equipment.items:
                if i.rectangle.collidepoint(mouse_position):
                    i.info_rectangle.bottomright = mouse_position
                    self.info_rectangle = i.info_rectangle
                    self.info_text = i.info_text
                    self.is_info_rectangle_visible = True
                    return True

        self.is_info_rectangle_visible = False
