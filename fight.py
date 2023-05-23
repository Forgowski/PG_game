import random
from settings import *
from button import Button

fight_background = pygame.image.load("assets/map/fight_background.png").convert()
FIGHT_BACKGROUND = pygame.transform.scale(fight_background, (WIDTH, HEIGHT))


class Fight:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.is_fighting = True
        self.first_strike = random.randint(0, 1)
        self.attack_button = Button(100, 25, WIDTH / 4, HEIGHT - 45, self.attack(self.player, self.enemy), "Attack",
                                    BUTTON_PNG)
        self.is_player_turn = self.first_strike
        self.main_loop()

    def draw(self):
        WIN.blit(FIGHT_BACKGROUND, (0, 0))
        WIN.blit(self.attack_button.image, self.attack_button.rectangle.topleft)
        WIN.blit(self.attack_button.rectangle_text, self.attack_button.rectangle_text_position)
        pygame.display.update()

    def handle_event(self):
        pass

    def attack(self, striker, target):
        if random.randint(1, 100) > target.stats.agility:
            target.update_hp(striker.stats.attack_power)
            if random.randint(1, 100) <= striker.stats.critical_damage_chance:
                # critical damage
                target.update_hp(striker.stats.attack_power)
        # miss
        else:
            pass

    def main_loop(self):
        while self.is_fighting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_fighting = False
            self.draw()

