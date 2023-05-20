import pygame.mixer

from settings import *
from button import Button

sound_button_jpg = pygame.transform.scale(pygame.image.load("assets/music/sound_button.png"),
                                          (25, 25))
arrow_right_button_jpg = pygame.transform.scale(pygame.image.load("assets/music/arrow_right_button.png"),
                                                (25, 25))
arrow_left_button_jpg = pygame.transform.scale(pygame.image.load("assets/music/arrow_left_button.png"),
                                               (25, 25))


class Sounds:
    def __init__(self):
        pygame.mixer.music.load("assets/music/soundtrack.mp3")
        self.sound = pygame.mixer.music
        self.sound.play(-1)
        self.left_arrow_button = Button(25, 25, 10, HEIGHT - 35, self.volume_down, None, arrow_left_button_jpg)
        self.sound_button = Button(25, 25, 40, HEIGHT - 35, self.stop_start_music, None, sound_button_jpg)
        self.right_arrow_button = Button(25, 25, 70, HEIGHT - 35, self.volume_up, None, arrow_right_button_jpg)
        self.buttons_list = [self.sound_button, self.right_arrow_button, self.left_arrow_button]

        pygame.mixer.music.set_volume(0.05)

    def draw(self):
        WIN.blit(self.left_arrow_button.image, self.left_arrow_button.rectangle.topleft)
        WIN.blit(self.sound_button.image, self.sound_button.rectangle.topleft)
        WIN.blit(self.right_arrow_button.image, self.right_arrow_button.rectangle.topleft)

    def volume_up(self):
        current_volume = self.sound.get_volume()
        self.sound.set_volume(current_volume + 0.05)

    def volume_down(self):
        current_volume = self.sound.get_volume()
        self.sound.set_volume(current_volume - 0.05)

    def stop_start_music(self):
        if self.sound.get_busy():
            self.sound.stop()
        else:
            self.sound.play(-1)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            for each in self.buttons_list:
                if each.rectangle.collidepoint(pygame.mouse.get_pos()):
                    each.onclick()
