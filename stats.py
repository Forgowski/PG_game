from settings import *

stats_background = pygame.image.load("assets/player/stats/stats_background.png").convert()
stats_background = pygame.transform.scale(stats_background, (300, 300))

upgrade_stats_png = pygame.image.load("assets/player/stats/upgrade_stats.png")


class Stats:
    def __init__(self, max_hp, attack_power, agility):
        self.max_hp = max_hp
        self.attack_power = attack_power
        self.agility = agility
        self.background = stats_background
        self.background_rectangle = self.background.get_rect()

    def level_up(self):
        self.max_hp += 20
        self.agility += 1
        self.attack_power += 20

    def agility_up(self, value):
        if self.agility + value > 75:
            self.agility = 75

        else:
            self.agility += value
