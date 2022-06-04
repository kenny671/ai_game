import pygame
from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load("images/alien.png")
        self.image = pygame.transform.scale(self.image,
            (ai_game.settings.screen_width // 16, ai_game.settings.screen_height // 12))
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.settings = ai_game.settings

    
    def update(self):
        self.x += self.settings.fleet_direction * self.settings.alien_speed_factor
        self.rect.x = self.x


    def check_edges(self):
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True