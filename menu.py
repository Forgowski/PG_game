from button import Button
from settings import *
from save import load_game

BUTTON_MENU_PNG = pygame.transform.scale(BUTTON_PNG, (300, 100))


class Menu:
    def __init__(self):
        self.is_open = True

        self.new_game_button = Button(300, 100, WIDTH / 2 - 150, HEIGHT / 2 - 200, self.new_game, None, BUTTON_MENU_PNG)
        self.new_game_button.rectangle_text = menu_bold_font.render("NEW GAME", True, (255, 255, 255))
        self.new_game_button.set_text_position()

        self.load_game_button = Button(300, 100, WIDTH / 2 - 150, HEIGHT / 2, self.load_game, None, BUTTON_MENU_PNG)
        self.load_game_button.rectangle_text = menu_bold_font.render("LOAD GAME", True, (255, 255, 255))
        self.load_game_button.set_text_position()

        self.exit_button = Button(300, 100, WIDTH / 2 - 150, HEIGHT / 2 + 200, self.exit, None, BUTTON_MENU_PNG)
        self.exit_button.rectangle_text = menu_bold_font.render("EXIT", True, (255, 255, 255))
        self.exit_button.set_text_position()

        self.wizard_button = Button(300, 100, WIDTH / 2 - 150, HEIGHT / 2, self.wizard, None, BUTTON_MENU_PNG)
        self.wizard_button.rectangle_text = menu_bold_font.render("Wizard", True, (255, 255, 255))
        self.wizard_button.set_text_position()

        self.knight_button = Button(300, 100, WIDTH / 2 - 150, HEIGHT / 2 - 200, self.knight, None, BUTTON_MENU_PNG)
        self.knight_button.rectangle_text = menu_bold_font.render("Knight", True, (255, 255, 255))
        self.knight_button.set_text_position()

        self.buttons_list = [self.new_game_button, self.load_game_button, self.exit_button]

        self.player = None
        self.boss = None
        self.player_type = None
        self.is_new_game = False

    def exit(self):
        if not self.is_new_game:
            exit()

    def wizard(self):
        self.player_type = "wizard"
        self.is_open = False

    def knight(self):
        self.player_type = "knight"
        self.is_open = False

    def load_game(self):
        if not self.is_new_game:
            is_ok, player, boss = load_game()
            self.player = player
            self.boss = boss

            if is_ok:
                self.is_open = False

    def new_game(self):
        if not self.is_new_game:
            self.is_new_game = True

    def event_handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if self.is_new_game:
                if self.wizard_button.is_pressed(pygame.mouse.get_pos()):
                    self.wizard_button.onclick()
                if self.knight_button.is_pressed(pygame.mouse.get_pos()):
                    self.knight_button.onclick()
            else:
                for button in self.buttons_list:
                    if button.is_pressed(pygame.mouse.get_pos()):
                        button.onclick()


    def draw(self):
        WIN.fill(BLACK)
        if self.is_new_game:
            WIN.blit(self.wizard_button.image, self.wizard_button.rectangle.topleft)
            WIN.blit(self.wizard_button.rectangle_text, self.wizard_button.rectangle_text_position)
            WIN.blit(self.knight_button.image, self.knight_button.rectangle.topleft)
            WIN.blit(self.knight_button.rectangle_text, self.knight_button.rectangle_text_position)
        else:
            for button in self.buttons_list:
                WIN.blit(button.image, button.rectangle.topleft)
                WIN.blit(button.rectangle_text, button.rectangle_text_position)
        pygame.display.update()

    def main_loop(self):
        clock = pygame.time.Clock()
        while self.is_open:
            clock.tick(5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_open = False
                    exit()
                self.event_handle(event)

            self.draw()

        if self.is_new_game:
            return 0, self.player_type, 0
        else:
            return 1, self.player, self.boss
