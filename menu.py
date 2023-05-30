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

        self.buttons_list = [self.new_game_button, self.load_game_button, self.exit_button]

        self.player = None
        self.opponents_level = None
        self.is_new_game = False

    @staticmethod
    def exit():
        exit()

    def load_game(self):

        is_ok, player = load_game()
        self.player = player

        if is_ok:
            self.is_open = False

    def new_game(self):
        self.is_new_game = True
        self.is_open = False

    def event_handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            for button in self.buttons_list:
                if button.is_pressed(pygame.mouse.get_pos()):
                    button.onclick()

    def draw(self):
        WIN.fill(BLACK)
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
                self.event_handle(event)

            self.draw()

        if self.is_new_game:
            return 0, 0
        else:
            return 1, self.player
