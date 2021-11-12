import pygame

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 850
        self.screen_height = 700 
        bg = pygame.image.load("blowfish.jpg")
        bg = pygame.transform.scale(bg, (self.screen_width, self.screen_height)) 
        self.bg = bg
        

        # Ship settings 
        self.ship_speed_x = 4.0
        self.ship_speed_y = 1.0
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 40
        self.bullet_height = 40
        self.bullet_color = (60,60,60,200)
        self.bullets_allowed = 5

        # Alien settings
        self.fleet_drop_speed = 10
        # fleet direction of 1 represents right, -1 left

        self.speedup_scale = 1.1

        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize things that change during the game"""

        self.ship_speed = 7.0
        self.bullet_speed = 3.0
        self.alien_speed = 5.0
        # fleet direction of 1 represents right, -1 left
        self.fleet_direction = 1
        #Scoring
        self.alien_points = 10

    def increase_speed(self):
        """Increases speeds"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

        