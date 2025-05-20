import pygame
from pygame.sprite import Sprite
from numpy import random
from utils import resource_path

class Bonus(Sprite):

    def __init__(self, ai_game, kind):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()
        self.kind = kind

        if kind == 'super':
            self.image = pygame.image.load(resource_path('images/super_bonus.bmp'))
        else:
            self.image = pygame.image.load(resource_path('images/multi_bonus.bmp'))

        self.speed = self.settings.bonus_speed

        self.rect = self.image.get_rect()
        self.rect.y = -self.screen_rect.height
        self.y = float(self.rect.x)
        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)

    def update(self):
        self.y += self.speed
        self.rect.y = self.y

    def blit_bonus(self):
        self.screen.blit(self.image, self.rect)


