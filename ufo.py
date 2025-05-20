import pygame
from pygame.sprite import Sprite
from numpy import random
from utils import resource_path
class Ufo(Sprite):
    '''A class for managing hostile UFOs'''
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = random.choice(self.settings.ufo_color)

        if self.color == 'r':
            self.image = pygame.image.load(resource_path('images/red_ufo.bmp'))
        elif self.color == 'g':
            self.image = pygame.image.load(resource_path('images/green_ufo.bmp'))
        elif self.color == 'b':
            self.image = pygame.image.load(resource_path('images/blue_ufo.bmp'))
        
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.settings.ufo_speed * self.settings.fleet_direction)
        self.rect.x = self.x

        


   