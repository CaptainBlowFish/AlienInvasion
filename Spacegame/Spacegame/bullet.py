import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired"""

    def __init__(self, ai_game, source, direction=1):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        self.source = source
        self.direction = direction

        self.bulletPic = pygame.image.load("ship.png")
        self.bulletPic = pygame.transform.scale(self.bulletPic, (self.settings.bullet_width,self.settings.bullet_height))

        # Create a bullet rect at (0,0) and then set correct position
        self.rect = pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        if self.direction == 1:
            self.rect.midtop = self.source.rect.midtop
        elif self.direction == -1:
            self.rect.midbottom = self.source.rect.midbottom
            self.bulletPic = pygame.transform.rotate(self.bulletPic, 180)
            


                

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        if self.direction == 1:
            self.y -= self.settings.bullet_speed
        elif self.direction == -1:
            self.y += self.settings.bullet_speed

        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        
        self.screen.blit(self.bulletPic, self.rect)