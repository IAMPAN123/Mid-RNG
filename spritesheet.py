import pygame

class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, color):
        # Create a new blank image with transparency
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        
        # Copy the sprite from the spritesheet onto the new image
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        
        # Scale the image if needed
        image = pygame.transform.scale(image, (width * scale, height * scale))
        
        # Set the color key for transparency
        image.set_colorkey(color)

        return image
