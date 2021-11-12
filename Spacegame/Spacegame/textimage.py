from pygame import font
import copy

class TextImage:
    """A class to report scoreings information"""
    
    def __init__(self, screen, text, style=None, size=20, text_color=(30,30,30), bg_color=None):
        """Initialize scorekeeping attributes"""
        self.screen = screen
        self.text = text
        self.style = style
        self.size = size
        
        self.screen_rect = self.screen.get_rect()

        # Font settings for scoring information
        self.text_color = copy.deepcopy(text_color)
        self.bg_color = copy.deepcopy(bg_color)
        self.font = font.SysFont(self.style, self.size)

        self.write(self.text)
        self.move(top=0, left=0)

    def write(self, text):
        """Change the text"""
        self.image = self.font.render(text, True, self.text_color, self.bg_color)

    def move(self, top=None, left=None, bottom=None, right=None):
        """Move the draw location"""
        rect = self.image.get_rect()

        if bottom != None:
            rect.bottom = bottom
        if right != None:
            rect.right = right
        if top != None:
            rect.top = top
        if left != None:
            rect.left = left

    def draw(self):
        """Draw the text to the screen."""
        self.screen.blit(self.image, self.image.get_rect())
