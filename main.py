import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from stats import GameStats
from button import Button
from georgiy import Georgiy
from scoreboard import Scoreboard
from time import sleep



class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.
            settings.screen_height))
        pygame.display.set_caption("SpaseInvaders")
        self.bg_image = pygame.image.load("images/space.png")
        self.bg_image = pygame.transform.scale(self.bg_image,
            (self.settings.screen_width, self.settings.screen_height))
        self.ship = Ship(self)
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.georgiy = Georgiy(self)


        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "START")


    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_georgiy()
                self.update_aliens()
                self._update_bullets()
                pygame.mouse.set_visible(False)
            else:
                self.aliens.empty()
                self.bullets.empty()
                self._create_fleet()
                self.stats.reset_stats()
                self.ship.center_ship()
                pygame.mouse.set_visible(False)
                self.sb.prep_score()

            self._update_screen()


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


    def _check_keydown_events(self, event):
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self.stats.game_active = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()


    def _check_keyup_events(self, event):
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_s:
            self.ship.moving_down = False

        
    def _update_screen(self):
        self.screen.blit(self.bg_image, (0, 0))
        self.ship.blitme()
        self.georgiy.draw()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.sb.show_score()


        pygame.display.flip()


    def _fire_bullet(self):
        if self.stats.game_active:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
            self.bullets.update()

            for bullet in self.bullets.copy():
                for bullet in self.bullets.copy():
                    if bullet.rect.top <= 0:
                        self.bullets.remove(bullet)
                self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

        if collisions:
            self.stats.score += self.settings.alien_points  
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()


    def _create_fleet(self):
        alien = Alien(self)
        al_w = alien.rect.width
        al_h = alien.rect.height
        avaible_space_x = self.settings.screen_width - (2 * al_w)
        number_aliens_x = avaible_space_x // (2 * al_w)
        number_rows = 3
        for row_n in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_n)


    def _create_alien(self, alien_number, row_n):
        alien = Alien(self)
        al_w, al_h = alien.rect.size
        alien.x = al_w + 2 * al_w * alien_number
        alien.rect.x = alien.x
        alien.y = al_h + 1.5 * al_w * row_n
        alien.rect.y = alien.y
        self.aliens.add(alien)


    def update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()


    def _check_fleet_edges(self):
        for alien in self.aliens:
            if alien.check_edges():
                self.change_fleet_direction()
                break


    def change_fleet_direction(self):
        for alien in self.aliens:
            alien.rect.y += self.settings.drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.hp > 0:
            self.stats.hp -= 1

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()


            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def  _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()
            self.settings.initialize_dynamic_settings()
            self.stats.game_active = True
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            self.sb.prep_score()
            

            pygame.mouse.set_visible(False)


    def _update_georgiy(self):
        x_ship, y_ship = self.ship.rect.center
        self.georgiy.update(x_ship, y_ship)

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game() 