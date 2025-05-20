import pygame
from pygame.sprite import Sprite
from utils import resource_path

class Spaceship(Sprite):
    '''A class for managing the player's spaceship'''

    def __init__(self, ai_game, player):
        super().__init__()
        self.screen = ai_game.screen #Insert alien_invasion.py's screen into local attribute for flexibility
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect() #Same with the game's screen rect

        if player:
            self.image = pygame.image.load(resource_path('images/spaceship.bmp'))
        else:
            self.image = pygame.image.load(resource_path('images/spaceship_lives.bmp'))

        self.rect = self.image.get_rect()
        
        #Place spaceship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.spaceship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.spaceship_speed
        
        self.rect.x = self.x

    def center_spaceship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)


    def blitme(self):

        #Draw spaceship at its current location
        self.screen.blit(self.image, self.rect)