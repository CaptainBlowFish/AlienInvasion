#EXTRAS
#Aliens shoot back
#boss
#less stolen art

import sys
import pygame
import time
import pickle
import random

from pygame import mouse
from pygame import mixer
from pygame.constants import MOUSEBUTTONDOWN
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

from textimage import TextImage

class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        mixer.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)


        # Make the play button
        self.play_button = Button(self,"play")

    def run_game(self):
        """Start the main loop for the game."""

        FPS = 30
        clock = pygame.time.Clock()

        fps_image = TextImage(self.screen, "", "courier new", 16, (0,0,0))
        fps_image.move(bottom=self.screen.get_rect().bottom, left=self.screen.get_rect().right/2)

        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

            fps_image.write(f'{clock.get_fps()}')
            fps_image.draw()

            pygame.display.flip()

            clock.tick(FPS)
    
    def _update_aliens(self):
        """Update the positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #look for aliens hitting bottom
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # treat same as if ship hit
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            
            # Decrement ships_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Pause 
            time.sleep(0.5)

            # Get rid of everything 
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
        else:
            #Make background special
            self.settings.bg = pygame.image.load("specialblowfish.xcf")
            self.settings.bg = pygame.transform.scale(self.settings.bg, (self.settings.screen_width, self.settings.screen_height))

            self.stats.game_active = False
            pygame.mouse.set_visible(True)

        

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens heve reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self):
        """Create the fleet of aliens"""
        #Make an alien
        alien = Alien(self,attack_frequency=10)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        available_space_x = self.settings.screen_width - (2 * alien_width)
        numbers_aliens_x = available_space_x // (2 * alien_width)

        #determine number of rows
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        max_rows = 6  

        # Create the fleet of aliens
        
        for row_number in range(number_rows):
            if row_number >= max_rows:
                break
            else:
                for alien_number in range(numbers_aliens_x):
                    self._create_alien(alien_number, row_number)
            
        self.aliens.add(alien)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row"""
        alien = Alien(self,attacks=True,attack_frequency=1)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        alien.x = alien_width + 2 * alien_width*alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.bottom >= self.settings.screen_height:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
        
        

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, False)
        
        if collisions:

            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                for alien in aliens:
                   alien.alien_hit()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.sb.check_high_score()

            mixer.music.load("explosion.wav")
            mixer.music.set_volume(0.5)
            mixer.music.play()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            
            #Increase level
            self.stats.level += 1
            self.sb.prep_level
    
    def _check_events(self):
        """Respond to keypresses and mouse events"""
        # Watch the keybaord and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pickle.dump(self.stats.high_score, open("High_score.p", "wb"))
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player click Play."""
        if not self.stats.game_active and self.play_button.rect.collidepoint(mouse_pos):
            # Reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_ships()
            pygame.mouse.set_visible(False)
            self.settings.initialize_dynamic_settings()
            self.settings.bg = pygame.image.load("blowfish.jpg")
            self.settings.bg = pygame.transform.scale(self.settings. bg, (self.settings.screen_width, self.settings.screen_height)) 

            # Clear the screen
            self.aliens.empty()
            self.bullets.empty()

            # Create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()
                
    def _check_keydown_events(self,event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True;
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True;
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True;
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True;
        elif event.key == pygame.K_q:
            sys.exit();
        elif event.key == pygame.K_SPACE:
            self._fire_bullet();
            
            mixer.music.load("jump.wav")
            mixer.music.set_volume(0.5)
            mixer.music.play()

    def _check_keyup_events(self,event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False;
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False;
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False;
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False;

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self,self.ship)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.blit(self.settings.bg,(0,0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        #draw the score information
        self.sb.show_score()

        #Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
    
    