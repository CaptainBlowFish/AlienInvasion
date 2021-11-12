import pygame

from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # set the player's initial starting point and size 
        self.image = pygame.image.load('alien.png')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store decimal values for the ships's horizontal and vertical positions
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Update the ship's postition base on the movement flags."""
        if self.moving_right == True and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed_x
        if self.moving_left == True and self.rect.left > 0:
            self.x -= self.settings.ship_speed_x
        if self.moving_up == True and self.rect.top  > 0:
            self.y -= self.settings.ship_speed_y
        if self.moving_down == True and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed_y
        
        #Update rect object from self.x, self.y
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw the player at its current location."""
        self.screen.blit(self.image, self.rect)
        