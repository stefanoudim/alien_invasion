import pygame.font
from pygame.sprite import Group
from spaceship import Spaceship

class Scoreboard:
    '''A class responsible for reporting soring info'''
    
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.game_stats = ai_game.game_stats

        self.text_color = (255, 255, 0)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
    
    def prep_score(self):
        #Turn the score into an image
        score_str = "{:,}".format(self.game_stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, None)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        #Turn the high score into an image
        high_score_str = "{:,}".format(self.game_stats.high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, None)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_new_high_score(self):
        #Call this every time a UFO is shot
        if self.game_stats.score > self.game_stats.high_score:
            self.game_stats.high_score = self.game_stats.score
            self.prep_high_score()


    def prep_ships(self):
        #Show how many spaceships are left
        self.spaceships = Group()
        for lives in range(self.game_stats.spaceships_left):
            spaceship = Spaceship(self.ai_game, False)
            spaceship.rect.x = 10 + lives * spaceship.rect.width
            spaceship.rect.y = 10
            self.spaceships.add(spaceship)

    def prep_level(self):
        level_str = str(self.game_stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, None)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.spaceships.draw(self.screen)