import sys, os
import pygame
from numpy import random
from time import sleep
from settings import Settings
from spaceship import Spaceship
from bullet import Bullet
from ufo import Ufo
from game_stats import GameStats
from bonus import Bonus
from button import Button
from scoreboard import Scoreboard
from logo import Logo
from utils import resource_path
    

class AlienInvasion:
    '''General class for managing game behavior'''
    
    def __init__(self):

        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.rect = self.screen.get_rect()

        self.screen_bg = pygame.image.load(resource_path('images/background.png'))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.screen_bg = pygame.transform.scale(self.screen_bg, (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        
        self.game_stats = GameStats(self)
        self.score_board = Scoreboard(self)
        self.spaceship = Spaceship(self, True)
        self.bullets = pygame.sprite.Group()
        self.ufos = pygame.sprite.Group()
        self.bonus = pygame.sprite.Group()

        self._create_fleet()
        self.play_button = Button(self, 'Play')
        self.logo = Logo(self, self.play_button)

    def run_game(self):

        while True:
            self._check_events()     #Check user input
           
            if self.game_stats.game_active:
                self.spaceship.update()   #Update object spaceship based on user input
                self._update_bullets()    #Update object bullets based on user input
                self._update_ufos()       #Update UFOs' motion 
                self._bonus_probability() #How often will bonuses appear?
                self._update_bonus()      #Responsible for bonus movement
                self._check_multi_bullet_timer() #Timer related method (that is why it has to be called constantly)

            self._update_screen()    #Draw screen

            
            

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.game_stats.reset_stats()
            self.game_stats.game_active = True
            self.score_board.prep_score()
            self.score_board.prep_level()
            self.score_board.prep_ships()

            self.ufos.empty()
            self.bullets.empty()
            self.bonus.empty()

            self._create_fleet()
            self.spaceship.center_spaceship()
            pygame.mouse.set_visible(False)
                    
                    
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.spaceship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.spaceship.moving_left = True
        elif event.key == pygame.K_q:
             self.game_stats.save_high_score()
             sys.exit()
        elif event.key == pygame.K_SPACE and self.game_stats.game_active:
             self._fire_bullet()
    
    def _check_keyup_events(self, event):
            if event.key == pygame.K_RIGHT:
                self.spaceship.moving_right = False
            elif event.key == pygame.K_LEFT:
                self.spaceship.moving_left = False

    def _fire_bullet(self):
         if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            new_bullet.bullet_sound.play()


         if self.settings.super_bullet:
            self.settings.super_bullet = False

    def _update_bullets(self):
        self.bullets.update()
        self._check_bullet_ufo_collisions()

        
    def _check_bullet_ufo_collisions(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
            hit_ufo = pygame.sprite.spritecollide(bullet, self.ufos, dokill=True)
            
            if hit_ufo and not bullet.is_super:
                self.bullets.remove(bullet)
            
            if hit_ufo:
                self.game_stats.score += self.settings.ufo_points * len(hit_ufo)
                self.score_board.prep_score()
                self.score_board.check_new_high_score()
                
            

        if not self.ufos:
            self.bullets.empty()
            self.bonus.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.game_stats.level += 1
            self.score_board.prep_level()


    def _create_fleet(self):
        ufo = Ufo(self)
        ufo_width, ufo_height = ufo.rect.size
        available_space_x = self.settings.screen_width - (2 * ufo_width)
        number_ufos_x = available_space_x // (2 * ufo_width)

        spaceship_height = self.spaceship.rect.height
        available_space_y = (self.settings.screen_height - 
                            (3 * ufo_height) - spaceship_height)
        number_rows = available_space_y // (2 * ufo_height)

        #Create full fleet (grid)
        for row_number in range(number_rows):
            for ufo_number in range(number_ufos_x):
                self._create_ufo(ufo_number, row_number)
            
    def _create_ufo(self, ufo_number, row_number):
        #Create hostile UFOs
        ufo = Ufo(self)
        ufo_width, ufo_height = ufo.rect.size
        ufo.x = ufo_width + 2 * ufo_width * ufo_number
        ufo.rect.x = ufo.x
        ufo.rect.y = ufo_height + 2 * ufo_height * row_number
        self.ufos.add(ufo)

    def _check_fleet_edges(self):
        for ufo in self.ufos.sprites():
            if ufo.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        for ufo in self.ufos.sprites():
            ufo.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _update_ufos(self):
        self._check_fleet_edges()
        self.ufos.update()

        if pygame.sprite.spritecollideany(self.spaceship, self.ufos):
            self._spaceship_hit()
        
        self._check_ufo_bottom()


    def _spaceship_hit(self):
        
        self.game_stats.spaceships_left -= 1
        if self.game_stats.spaceships_left > 0:

            self.score_board.prep_ships()
            self.ufos.empty()
            self.bullets.empty()
            self.bonus.empty()

            self._create_fleet()
            self.spaceship.center_spaceship()

            sleep(1.0)
        else:
            self.score_board.prep_ships()
            self.game_stats.game_active = False
            self.game_stats.save_high_score()
            pygame.mouse.set_visible(True)

    def _check_ufo_bottom(self):
        screen_rect = self.screen. get_rect()
        for ufo in self.ufos.sprites():
            if ufo.rect.bottom > screen_rect.bottom:
                self._spaceship_hit()

    def _bonus_probability(self):
        if random.random() < self.settings.bonus_probability:  
            self._spawn_bonus()


    def _check_bonus_spaceship_collisions(self):
        for bonus in self.bonus.copy():
            if bonus.rect.top >= self.rect.bottom:
                self.bonus.remove(bonus)
        
        for bonus in pygame.sprite.spritecollide(self.spaceship, self.bonus, dokill=False):
            if bonus.kind == 'multi':
                self.settings.multi_bullets_bonus_active = True
                self.settings.bullets_allowed = self.settings.multi_bullets_bonus_number
                self.settings.multi_bullets_start_time = pygame.time.get_ticks()
            elif bonus.kind == 'super':
                self.settings.super_bullet = True
            
            bonus.kill()

            
    def _spawn_bonus(self):
        kind = random.choice(['multi', 'super'])
        bonus = Bonus(self, kind)
        self.bonus.add(bonus)


    def _update_bonus(self):
        self.bonus.update()
        self._check_bonus_spaceship_collisions()

    def _check_multi_bullet_timer(self):
        if self.settings.multi_bullets_bonus_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.settings.multi_bullets_start_time >= self.settings.multi_bullets_duration:
                self.settings.multi_bullets_bonus_active = False
                self.settings.bullets_allowed = self.settings.default_bullets_allowed

    def _update_screen(self):
        self.screen.blit(self.screen_bg, self.rect)
        self.spaceship.blitme()
        
        for bullet in self.bullets.sprites():
             bullet.blit_bullet()
        
        self.ufos.draw(self.screen)
        self.score_board.show_score()

        for bonus in self.bonus.sprites():
            bonus.blit_bonus()
        
        if not self.game_stats.game_active:
            self.play_button.draw_button()
            self.logo.blit_logo()

        pygame.display.flip()
    
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()