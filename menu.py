from button import Button
from settings import *

BUTTON_MENU_PNG = pygame.transform.scale(BUTTON_PNG, (300, 100))


class Menu:
    def __init__(self):
        self.new_game_button = Button(300, 100, WIDTH / 2 - 150, HEIGHT / 2 - 200, None, None, BUTTON_MENU_PNG)
        self.new_game_button.rectangle_text = menu_bold_font.render("NEW GAME", True, (255, 255, 255))
        self.new_game_button.set_text_position()
        self.is_open = True
        self.load_game_button = Button(300, 100, WIDTH / 2 - 150, HEIGHT / 2, None, None, BUTTON_MENU_PNG)
        self.load_game_button.rectangle_text = menu_bold_font.render("LOAD GAME", True, (255, 255, 255))
        self.load_game_button.set_text_position()
        self.main_loop()

    def event_handle(self):
        pass

    def draw(self):
        WIN.fill(BLACK)
        WIN.blit(self.new_game_button.image, self.new_game_button.rectangle.topleft)
        WIN.blit(self.new_game_button.rectangle_text, self.new_game_button.rectangle_text_position)
        WIN.blit(self.load_game_button.image, self.load_game_button.rectangle.topleft)
        WIN.blit(self.load_game_button.rectangle_text, self.load_game_button.rectangle_text_position)
        pygame.display.update()

    def main_loop(self):
        clock = pygame.time.Clock()
        while self.is_open:
            clock.tick(5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_open = False

            self.draw()
