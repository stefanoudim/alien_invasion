class Settings:
    '''A class responsible for all project settings'''
    def __init__(self):

      # -- STATIC SETTINGS -- #

        # SCREEN SETTINGS
        self.screen_width = 1200
        self.screen_height = 700

        #SPACESHIP SETTINGS
        self.spaceships_limit = 3

        #BULLET SETTINGS
        self.default_bullets_allowed = 2
        self.bullets_allowed = self.default_bullets_allowed

        #UFO SETTINGS
        self.ufo_color = ['r', 'g', 'b']
        self.fleet_drop_speed = 15

        #BONUS SETTINGS
        self.multi_bullets_bonus_number = 8
        self.multi_bullets_duration = 2000  # 2 seconds 

        #GAME SETTINGS
        self.speedup_scale = 1.1
        self.bonus_probability_increase = 1.1
        self.score_scale = 1.5

      # -- DYNAMIC SETTINGS -- #
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.spaceship_speed = 1.5
        self.bullet_speed = 1.5
        self.ufo_speed = 1.0
        self.bonus_speed = 0.7
        self.fleet_direction = 1 #1 -> right, -1 -> left
        self.multi_bullets_start_time = None
        self.super_bullet = False
        self.multi_bullets_bonus_active = False
        self.bonus_probability = 0.00008
        self.ufo_points = 50


    def increase_speed(self):
        self.spaceship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.ufo_speed *= self.speedup_scale
        self.bonus_speed *= self.speedup_scale
        self.bonus_probability *= self.bonus_probability_increase
        self.ufo_points = int(self.ufo_points * self.score_scale)    

