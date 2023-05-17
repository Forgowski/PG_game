from settings import *
from button import Button

stats_background = pygame.image.load("assets/player/stats/stats_background.png").convert()
stats_background = pygame.transform.scale(stats_background, (400, 400))

upgrade_stats_png = pygame.image.load("assets/player/stats/upgrade_stats.png").convert()
upgrade_stats_png = pygame.transform.scale(upgrade_stats_png, (20, 20))


class Stats:
    def __init__(self, max_hp, attack_power, agility, critical_damage):
        self.max_hp = max_hp
        self.critical_damage = critical_damage
        self.attack_power = attack_power
        self.agility = agility
        self.is_visible = False

        self.upgrade_points = 0

        self.background_pos_x = WIDTH / 2 - 200
        self.background_pos_y = HEIGHT / 2 - 200
        self.background = stats_background
        self.background_rectangle = self.background.get_rect()
        self.background_rectangle.topleft = (self.background_pos_x, self.background_pos_y)

        self.upgrade_Stats_png_rectangle = upgrade_stats_png.get_rect()
        self.max_hp_button = Button(self.upgrade_Stats_png_rectangle.width, self.upgrade_Stats_png_rectangle.height,
                                    self.background_pos_x + 270, self.background_pos_y + 80, self.max_hp_up, None,
                                    upgrade_stats_png)
        self.max_hp_text = stats_font.render(f"max HP: {self.max_hp}", True, (255, 255, 255))

        self.attack_power_button = Button(self.upgrade_Stats_png_rectangle.width,
                                          self.upgrade_Stats_png_rectangle.height,
                                          self.background_pos_x + 270, self.background_pos_y + 145,
                                          self.attack_power_up,
                                          None, upgrade_stats_png)
        self.attack_power_text = stats_font.render(f"attack power: {self.attack_power}", True, (255, 255, 255))

        self.agility_button = Button(self.upgrade_Stats_png_rectangle.width, self.upgrade_Stats_png_rectangle.height,
                                     self.background_pos_x + 270, self.background_pos_y + 210, self.agility_up, None,
                                     upgrade_stats_png)
        self.agility_text = stats_font.render(f"agility points: {self.agility}", True, (255, 255, 255))

        self.critical_damage_button = Button(self.upgrade_Stats_png_rectangle.width,
                                             self.upgrade_Stats_png_rectangle.height,
                                             self.background_pos_x + 270, self.background_pos_y + 275,
                                             self.critical_damage_up, None, upgrade_stats_png)
        self.critical_damage_text = stats_font.render(f"critical damage chance: {self.critical_damage}", True,
                                                      (255, 255, 255))

        self.available_points_text = stats_font.render(f"available points: {self.upgrade_points}", True,
                                                       (255, 255, 255))

    def level_up(self):
        self.max_hp += 20
        self.agility += 1
        self.attack_power += 20

    def agility_check(self, value):
        if self.agility + value > 75:
            self.agility = 75

        else:
            self.agility += value

    def agility_up(self):
        pass

    def critical_damage_up(self):
        pass

    def max_hp_up(self):
        pass

    def attack_power_up(self):
        pass

    def draw(self):
        WIN.blit(self.background, self.background_rectangle.topleft)
        WIN.blit(self.agility_button.image, self.agility_button.rectangle.topleft)
        WIN.blit(self.critical_damage_button.image, self.critical_damage_button.rectangle.topleft)
        WIN.blit(self.max_hp_button.image, self.max_hp_button.rectangle.topleft)
        WIN.blit(self.attack_power_button.image, self.attack_power_button.rectangle.topleft)

        WIN.blit(self.max_hp_text,
                 (self.max_hp_button.rectangle.topleft[0] - 220, self.max_hp_button.rectangle.topleft[1]))

        WIN.blit(self.critical_damage_text, (
            self.critical_damage_button.rectangle.topleft[0] - 220, self.critical_damage_button.rectangle.topleft[1]))

        WIN.blit(self.attack_power_text,
                 (self.attack_power_button.rectangle.topleft[0] - 220, self.attack_power_button.rectangle.topleft[1]))

        WIN.blit(self.agility_text,
                 (self.agility_button.rectangle.topleft[0] - 220, self.agility_button.rectangle.topleft[1]))

        WIN.blit(self.available_points_text, (WIDTH / 2 - self.available_points_text.get_rect().width / 2,
                                              self.critical_damage_button.rectangle.topleft[1] + 45))

    def event_handle(self):
        pass
