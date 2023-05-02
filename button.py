from settings import *


class Button:
    def __init__(self, width, height, x, y, onclick, text):
        self.rectangle = pygame.Rect(x, y, width, height)
        self.rectangle_text = my_bold_font.render(text, True, (255, 255, 255))
        self.rectangle_text_position = (0, 0)
        self.onclick = onclick

    def is_pressed(self, mouse_position):
        if self.rectangle.collidepoint(mouse_position):
            self.onclick()
