from settings import *


class Button:
    def __init__(self, width, height, x, y, onclick, text, image=None):
        self.rectangle = pygame.Rect(x, y, width, height)
        self.rectangle_text = my_bold_font.render(text, True, (255, 255, 255))
        self.rectangle_text_position = (0, 0)
        self.onclick = onclick
        self.text_position_x = None
        self.text_position_y = None
        self.rectangle_text_position = None
        self.image = image
        self.set_text_position()

    def is_pressed(self, mouse_position):
        if self.rectangle.collidepoint(mouse_position):
            self.onclick()

    def set_text_position(self):
        self.text_position_x = (self.rectangle.width - (
            self.rectangle_text.get_width())) / 2 + self.rectangle.x

        self.text_position_y = (self.rectangle.height / 2 - (
                self.rectangle_text.get_height() / 2)) + self.rectangle.y

        self.rectangle_text_position = (self.text_position_x, self.text_position_y)

    def draw(self):
        WIN.blit(self.image, self.rectangle.topleft)
        WIN.blit(self.rectangle_text, self.rectangle_text_position)
