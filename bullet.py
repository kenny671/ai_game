import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_right = False
        self.moving_left  = False
        
        if ai_game.ship.moving_right:
            self.moving_right = True
        if ai_game.ship.moving_left:
            self.moving_left = True



    def update(self):
        if self.moving_right:
            self.x += self.settings.bullet_speed_factor
        if self.moving_left:
            self.x -= self.settings.bullet_speed_factor
        self.rect.x = self.x

        self.y -= self.settings.bullet_speed_factor
        self.rect.y = self.y



    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)