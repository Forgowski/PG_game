from settings import *
from equipment import Equipment

knight = [pygame.image.load("assets/player/knight/knight.png"),
          pygame.image.load("assets/player/knight/knight2.png"),
          pygame.image.load("assets/player/knight/knight3.png"),
          pygame.image.load("assets/player/knight/knight4.png"),
          pygame.image.load("assets/player/knight/knight5.png"),
          ]

wizzard = [pygame.image.load("assets/player/wizzard/wizzard.png"),
           pygame.image.load("assets/player/wizzard/wizzard2.png"),
           pygame.image.load("assets/player/wizzard/wizzard3.png"),
           pygame.image.load("assets/player/wizzard/wizzard4.png"),
           pygame.image.load("assets/player/wizzard/wizzard5.png"),
           ]

enemy = [pygame.image.load("assets/player/enemy/enemy.png"),
         pygame.image.load("assets/player/enemy/enemy2.png"),
         pygame.image.load("assets/player/enemy/enemy3.png"),
         pygame.image.load("assets/player/enemy/enemy4.png"),
         pygame.image.load("assets/player/enemy/enemy5.png"),

         ]

knight_death = [pygame.image.load("assets/player/knight/knight_d.png"),
                pygame.image.load("assets/player/knight/knight_d1.png"),
                pygame.image.load("assets/player/knight/knight_d2.png"),
                pygame.image.load("assets/player/knight/knight_d3.png"),
                ]

wizzard_death = [pygame.image.load("assets/player/wizzard/wizzard_d.png"),
                 pygame.image.load("assets/player/wizzard/wizzard_d1.png"),
                 pygame.image.load("assets/player/wizzard/wizzard_d2.png"),
                 pygame.image.load("assets/player/wizzard/wizzard_d3.png"),
                 ]


class Character(pygame.sprite.Sprite):
    def __init__(self, hero_type):
        super().__init__()
        if hero_type == "knight":
            self.images = knight
            self.death_images = knight_death
        else:
            self.images = wizzard
            self.death_images = wizzard_death

        self.is_alive = True
        self.lvl = 1

        self.hp = 100
        self.exp = 0

        self.hp_bar = pygame.Rect(30, 10, 100, 15)
        self.hp_background_bar = pygame.Rect(30, 10, 100, 15)
        self.exp_to_next_level = 100
        self.exp_bar = pygame.Rect(30, 30, 0, 15)
        self.exp_background_bar = pygame.Rect(30, 30, 100, 15)

        self.current_image = 0
        self.current_death_image = 0
        self.image = self.images[self.current_image]

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.make_slower = 6
        self.counter = 0
        self.death_frame_counter = 0

        self.equipment = Equipment(hero_type)

    def update(self):
        if self.counter % self.make_slower == 0:
            self.current_image += 1
            if self.current_image >= len(self.images):
                self.current_image = 0
            self.image = self.images[self.current_image]
            self.counter = 0
        self.counter += 1

    def change_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update_hp_bar(self, value):
        if self.hp - value <= 0:
            self.hp -= value
            self.hp_bar.width = self.hp
            self.is_alive = False
            return True

        self.hp -= value
        self.hp_bar.width = self.hp

    def update_exp_bar(self, value):
        if self.exp + value >= self.exp_to_next_level:
            self.exp_bar.width = 0
            self.lvl += 1
            self.exp = 0
            self.exp_to_next_level = 100 * 2 * self.lvl
        self.exp += value
        self.exp_bar.width = int(self.exp / self.exp_to_next_level * 100)

    def death_animation(self):
        if self.death_frame_counter % self.make_slower * 4 == 0:
            self.image = self.death_images[self.current_death_image]
            if self.current_death_image < len(self.death_images) - 1:
                self.current_death_image += 1

        self.death_frame_counter += 1

    def revive(self):
        self.is_alive = True
        self.hp = 1
        self.update_hp_bar(0)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hp = opponents_level * 100
        self.attack_power = opponents_level * 20
        self.images = enemy
        self.current_image = 4
        self.exp_drop = opponents_level * 20
        self.image = self.images[self.current_image]
        self.rect = (self.image.get_rect())
        self.rect.x = 0
        self.rect.y = 0

    def change_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
