import random

from settings import *
from button import Button

fight_background = pygame.image.load("assets/map/fight_background.png").convert()
FIGHT_BACKGROUND = pygame.transform.scale(fight_background, (WIDTH, HEIGHT))

sword_attack = [pygame.transform.scale(pygame.image.load("assets/player/sword_attack/A200-1.png"), (25, 35)),
                pygame.transform.scale(pygame.image.load("assets/player/sword_attack/A200-2.png"), (25, 35)),
                pygame.transform.scale(pygame.image.load("assets/player/sword_attack/A200-3.png"), (25, 35)),
                pygame.transform.scale(pygame.image.load("assets/player/sword_attack/A200-4.png"), (25, 35)),
                ]


class Fight:
    def __init__(self, player, enemy):
        self.player_potion = None
        self.player = player
        self.player_position = (WIDTH / 4, HEIGHT / 2)
        self.enemy = enemy
        self.enemy_position = (WIDTH / 4 * 3, HEIGHT / 2)
        self.is_fighting = True
        self.attack_button = Button(100, 25, WIDTH / 4, HEIGHT - 45, lambda: self.attack(self.player, self.enemy),
                                    "Attack", BUTTON_PNG)
        self.hp_potion_button = Button(100, 25, WIDTH / 4 * 3, HEIGHT - 45, self.use_potion,
                                       "HP potion", BUTTON_PNG)
        self.available_potions = self.check_potions()
        self.available_potions_text = my_bold_font.render(f'Available potions: {self.available_potions}', True,
                                                          (255, 255, 255))
        self.is_player_turn = random.randint(0, 1)

        self.animation_frame = sword_attack[0]
        self.animation_generator = self.sword_attack_animation_gen()
        self.animation_counter = 0
        self.animation_cords = None

        self.main_loop()

    def draw(self):
        WIN.blit(FIGHT_BACKGROUND, (0, 0))
        WIN.blit(self.attack_button.image, self.attack_button.rectangle.topleft)
        WIN.blit(self.attack_button.rectangle_text, self.attack_button.rectangle_text_position)
        WIN.blit(self.hp_potion_button.image, self.hp_potion_button.rectangle.topleft)
        WIN.blit(self.hp_potion_button.rectangle_text, self.hp_potion_button.rectangle_text_position)
        WIN.blit(self.available_potions_text, (self.hp_potion_button.rectangle.topright[0] + 10, HEIGHT - 42))
        WIN.blit(self.player.image, self.player_position)
        WIN.blit(self.enemy.image, self.enemy_position)
        self.player.update_hp_bar()
        self.enemy.update_hp_bar()
        pygame.draw.rect(WIN, CLARET, self.player.hp_background_bar)
        pygame.draw.rect(WIN, RED, self.player.hp_bar)
        pygame.draw.rect(WIN, CLARET, self.enemy.hp_background_bar)
        pygame.draw.rect(WIN, RED, self.enemy.hp_bar)
        if self.animation_counter > 0:
            self.sword_attack_animation()
            WIN.blit(self.animation_frame, self.animation_cords)

        pygame.display.update()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if event.button == pygame.BUTTON_LEFT:
                if self.attack_button.rectangle.collidepoint(mouse_position):
                    self.attack_button.onclick()
                if self.hp_potion_button.rectangle.collidepoint(mouse_position):
                    self.hp_potion_button.onclick()

    def use_potion(self):
        if self.is_player_turn and self.available_potions > 0:
            self.available_potions -= 1
            self.available_potions_text = my_bold_font.render(f'Available potions: {self.available_potions}', True,
                                                              (255, 255, 255))
            self.player_potion.use(self.player)
            self.player.equipment.item_used(self.player_potion)
            self.is_player_turn = 0

    def check_potions(self):
        potion_number = 0
        for item in self.player.equipment.items:
            if item.name == 'hp_potion':
                self.player_potion = item
                potion_number = item.amount
        if potion_number > 3:
            return 3
        else:
            return potion_number

    def attack(self, striker, target):
        if self.animation_counter == 0:
            if self.is_player_turn:
                self.animation_cords = self.enemy_position
            else:
                self.animation_cords = self.player_position
            self.animation_counter += 4
            if random.randint(1, 100) > target.stats.agility:
                target.update_hp(striker.stats.attack_power)
                if random.randint(1, 100) <= striker.stats.critical_damage_chance:
                    # critical damage
                    target.update_hp(striker.stats.attack_power)
            # miss
            else:
                pass
            self.is_player_turn = not self.is_player_turn

    @staticmethod
    def sword_attack_animation_gen():
        num = 0
        while True:
            yield num
            num = (num + 1) % 4

    def sword_attack_animation(self):
        self.animation_frame = sword_attack[next(self.animation_generator)]
        self.animation_counter -= 1

    def main_loop(self):
        clock = pygame.time.Clock()
        while self.is_fighting:
            clock.tick(5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_fighting = False
                self.handle_event(event)
            if not self.is_player_turn:
                self.attack(self.enemy, self.player)

            if not self.player.is_alive or not self.enemy.is_alive and self.animation_counter == 0:
                self.is_fighting = False
            self.draw()
