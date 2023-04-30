import pygame
import pyrect

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


class Character(pygame.sprite.Sprite):
    def __init__(self, player_type):
        super().__init__()
        if player_type == "knight":
            self.images = knight
        else:
            self.images = wizzard
        self.hp = 100
        self.hp_bar = pygame.Rect(10, 10, 100, 10)
        self.hp_background_bar = pygame.Rect(10, 10, 100, 10)
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.make_slower = 4
        self.counter = 0

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

    def update_hp_bar(self):
        self.hp_bar.width = self.hp


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = enemy
        self.current_image = 4
        self.image = self.images[self.current_image]
        self.rect = (self.image.get_rect())
        self.rect.x = 0
        self.rect.y = 0

    def change_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
