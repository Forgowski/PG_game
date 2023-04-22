import pygame

knight = [pygame.image.load("assets/player/knight/knight.png"),
            pygame.image.load("assets/player/knight/knight2.png"),
            pygame.image.load("assets/player/knight/knight3.png"),
            pygame.image.load("assets/player/knight/knight4.png"),
            pygame.image.load("assets/player/knight/knight5.png"),
          ]
knight_death = [pygame.image.load("assets/player/knight/knight_d.png"),
                pygame.image.load("assets/player/knight/knight_d1.png"),
                pygame.image.load("assets/player/knight/knight_d2.png"),
                pygame.image.load("assets/player/knight/knight_d3.png"),
                ]
wizzard= [pygame.image.load("assets/player/wizzard/wizzard.png"),
            pygame.image.load("assets/player/wizzard/wizzard2.png"),
            pygame.image.load("assets/player/wizzard/wizzard3.png"),
            pygame.image.load("assets/player/wizzard/wizzard4.png"),
            pygame.image.load("assets/player/wizzard/wizzard5.png"),
          ]
wizzard_death = [pygame.image.load("assets/player/wizzard/wizzard_d.png"),
                pygame.image.load("assets/player/wizzard/wizzard_d1.png"),
                pygame.image.load("assets/player/wizzard/wizzard_d2.png"),
                pygame.image.load("assets/player/wizzard/wizzard_d3.png"),
                ]


class Character(pygame.sprite.Sprite):
    def __init__(self, player_type):
        super().__init__()
        if player_type == "knight":
            self.images = knight
        else:
            self.images = wizzard
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        self.current_image += 1
        if self.current_image >= len(self.images):
            self.current_image = 0
        self.image = self.images[self.current_image]