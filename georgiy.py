import pygame
from pygame.sprite import Sprite

class Georgiy(Sprite):
    def __init__(self, ai_game):    
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load("images/georgiy.png")
        self.image = pygame.transform.scale(self.image,
            (ai_game.settings.screen_width // 16, ai_game.settings.screen_height // 12))
        self.color = (255, 255, 255)

        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.rect.center = (200, 200)

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.r = 1
    

    def update(self, x_ship, y_ship):
        x_ge, y_ge = self.rect.center
        a = x_ge - x_ship
        b = y_ge - y_ship
        R = (a ** 2 + b ** 2) ** .5
        dx = a * self.r / R
        dy = b * self.r / R

        self.x -= dx
        self.rect.x = self.x
        self.y -= dy
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)





