class Settings():

    def __init__(self):

        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (25, 25, 112)

        self.bullet_speed = 7
        self.bullet_h_speed = 1.05
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = (0, 0, 128)

        self.alien_speed = 3
        self.drop_speed = 10

        self.ship_limit = 3


        self.speedup_scale  = 1.1

        self.score_scale = 1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
     self.ship_speed_factor = 5
     self.bullet_speed_factor = 10
     self.alien_speed_factor = 4


     self.fleet_direction = 1

     self.alien_points = 50


    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
    
        
      