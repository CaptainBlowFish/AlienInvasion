import pygame
from pygame.sprite import Sprite
from bullet import Bullet
import random

class Alien(Sprite):
    """Initialize the alien and set its starting position."""

    def __init__(self, ai_game, health=1, image="BlueFish.png", attacks=False, attack_frequency=0):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings=ai_game.settings
        self.ai_game = ai_game

        #Load the alien image and set its rect attribute.
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (int(self.settings.screen_width/25), int(self.settings.screen_height/20)))
        self.rect = self.image.get_rect()
        
        self.hp = health
        self.attacks = attacks
        self.attack_frequency = attack_frequency

        #Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the alien's exact horizontal position.
        self.x = float(self.rect.x)
        
    def update(self):
        """Move alien to the right or left"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
        if self.attacks == True:
            if self.attack_frequency >=random.randint(1,110):
                new_bullet = Bullet(self,self, -1)
                self.ai_game.bullets.add(new_bullet)
                

    def check_edges(self):
        """Return true if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        else:
            return False
    def alien_hit(self):
        """Removes health and removes the alien if health <= 0"""
        self.hp -= 1

        if self.hp <= 0:
            self.kill()