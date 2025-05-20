import pygame
from utils import resource_path

class Logo:

    def __init__(self, ai_game, play_button):
        self.screen = ai_game.screen

        self.image = pygame.image.load(resource_path('images/game_logo.png'))
        width = self.screen.get_rect().width // 2
        height = self.screen.get_rect().height // 2
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

        self.rect.centerx = play_button.rect.centerx
        self.rect.bottom = play_button.rect.top - 30 
    
    def blit_logo(self):
        self.screen.blit(self.image, self.rect)
