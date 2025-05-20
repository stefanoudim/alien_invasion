import pygame
from pygame.sprite import Sprite
from utils import resource_path

class Bullet(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        if not self.settings.super_bullet:
            self.image = pygame.image.load(resource_path('images/bullet.bmp'))
            self.bullet_sound = pygame.mixer.Sound(resource_path('sounds/simple_bullet.wav'))
        else:
            self.image = pygame.image.load(resource_path('images/super_bullet.bmp'))
            self.bullet_sound = pygame.mixer.Sound(resource_path('sounds/super_bullet.wav'))
            
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.spaceship.rect.midtop

        self.y = float(self.rect.y)
        self.is_super = self.settings.super_bullet

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def blit_bullet(self):
        self.screen.blit(self.image, self.rect)
