import pygame

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1500
        self.screen_height = 800 
        bg = pygame.image.load("blowfish.jpg")
        bg = pygame.transform.scale(bg, (self.screen_width, self.screen_height)) 
        self.bg = bg
        

        # Ship settings 
        self.ship_speed = 4
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 40
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 1000

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet direction of 1 represents right, -1 left
        self.fleet_direction = 1

        