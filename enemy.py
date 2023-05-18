from settings import *

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
        self.max_hp = 100
        self.hp = 100
        self.is_alive = True
        self.attack_power = 10
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

    def heal(self):
        self.hp = self.max_hp

    def change_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def level_up(self):
        self.lvl += 1
        self.max_hp = self.lvl * 100
        self.hp = self.lvl * 100
        self.attack_power = self.lvl * 10
        self.exp_drop = self.lvl * 20
        self.gold_drop = self.lvl * 1
