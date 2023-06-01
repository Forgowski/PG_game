from enemy import *

boss_png = pygame.transform.scale(pygame.image.load("assets/player/bos/boss.png"), (45, 55))


class Boss(Enemy):
    def __init__(self, level):
        super().__init__(1)
        self.is_alive = False
        self.stats = Stats(1000, 50, 30, 50)
        self.hp = 1000
        self.exp_drop = 500
        self.gold_drop = 50
        self.info_bar_background = None
        self.enemies_to_boss = 50
        self.info_bar_text = my_font.render(f'enemies to boss {self.enemies_to_boss}', True, (255, 255, 255))
        self.info_bar_rectangle = self.info_bar_text.get_rect()
        self.info_bar_rectangle.topleft = (WIDTH - self.info_bar_rectangle.width - 20, 20)
        self.image = boss_png
        self.rect = (self.image.get_rect())
        self.rect.x = 1590
        self.rect.y = 1920
        while self.lvl < level:
            self.level_up()

    def level_up(self):
        self.lvl += 1
        self.stats.max_hp *= 2
        self.hp *= 2
        self.stats.attack_power *= 2
        self.exp_drop *= 3
        self.gold_drop *= 3

    def update_info_bar(self):
        self.info_bar_text = my_font.render(f'enemies to boss: {self.enemies_to_boss}', True, (255, 255, 255))
        self.info_bar_rectangle = self.info_bar_text.get_rect()
        self.info_bar_rectangle.topleft = (WIDTH - self.info_bar_rectangle.width - 20, 20)

    def draw_info_bar(self):
        self.update_info_bar()
        pygame.draw.rect(WIN, BLACK, self.info_bar_rectangle)
        WIN.blit(self.info_bar_text, self.info_bar_rectangle)

    def update_is_alive(self):
        self.enemies_to_boss -= 1
        if self.enemies_to_boss < 0:
            self.enemies_to_boss = 0
        if self.enemies_to_boss == 0:
            self.is_alive = True
            self.hp = self.stats.max_hp

    def boss_defeated(self):
        self.enemies_to_boss = 50
        self.level_up()

    def draw(self):
        self.draw_info_bar()
        if self.is_alive:
            WIN.blit(self.image, self.rect)
