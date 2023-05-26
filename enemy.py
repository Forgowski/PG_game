from settings import *
from stats import Stats

enemy = [pygame.image.load("assets/player/enemy/enemy.png"),
         pygame.image.load("assets/player/enemy/enemy2.png"),
         pygame.image.load("assets/player/enemy/enemy3.png"),
         pygame.image.load("assets/player/enemy/enemy4.png"),
         pygame.image.load("assets/player/enemy/enemy5.png"),

         ]


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.lvl = 1
        self.stats = Stats(100, 10, 20, 20)
        self.hp = 100
        self.hp_bar = pygame.Rect(WIDTH - 130, 10, 100, 15)
        self.hp_background_bar = pygame.Rect(WIDTH - 130, 10, 100, 15)
        self.is_alive = True
        self.images = enemy
        self.current_image = 4
        self.exp_drop = 20
        self.gold_drop = 1
        self.image = self.images[self.current_image]
        self.rect = (self.image.get_rect())
        self.rect.x = 0
        self.rect.y = 0

    def update_hp(self, value):
        self.hp -= value
        if self.hp < 0:
            self.is_alive = False

    def update_hp_bar(self):
        self.hp_bar.width = self.hp / self.stats.max_hp * 100

    def heal(self):
        self.hp = self.stats.max_hp

    def change_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def level_up(self):
        self.lvl += 1
        self.stats.max_hp *= 1.5
        self.hp *= 1.5
        self.stats.attack_power *= 1.5
        self.exp_drop *= 1.5
        self.gold_drop = self.lvl * 1
