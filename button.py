import pygame

pygame.mixer.init()

#load sound
button_sound = pygame.mixer.Sound("Audio/clicks.mp3")

#Define
class Button():
    #load img
    def __init__(self, x, y, image, width=None, height=None, effect_enabled=True):
        if width and height:
            self.original_image = pygame.transform.scale(image,(width, height))
        else:
            self.original_image = image
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(x,y))
        self.original_rect = self.rect.copy()#save original for use when restore
        self.clicked = False
        self.effect_enabled = effect_enabled 

        # Create a mask for the button's image to match its shape
        self.mask = pygame.mask.from_surface(self.original_image)

        # darken effect duration
        self.darken_duration =500  
        self.darken_start_time = None  

        self.button_enabled = True 

    #draw img
    def draw(self, screen):
        action = False

        # Only process input if the button is enabled
        if self.button_enabled:
            # Get mouse position
            pos = pygame.mouse.get_pos()

            # Check mouseover and clicked conditions
            if self.rect.collidepoint(pos) and self.mask.get_at((pos[0] - self.rect.x, pos[1] - self.rect.y)):
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                    self.clicked = True

                    if self.effect_enabled:
                        # Apply shrink effect
                        scale_factor = 0.95  
                        new_width = int(self.rect.width * scale_factor)
                        new_height = int(self.rect.height * scale_factor)

                        # Calculate new position
                        center = self.rect.center 
                        self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
                        self.rect = self.image.get_rect(center=center)   # Update the rect to new size and position

                        # Apply darken effect
                        darken_image = pygame.Surface(self.image.get_size(), pygame.SRCALPHA) 
                        for x in range(self.image.get_width()):
                            for y in range(self.image.get_height()):
                                # Darken opaque area
                                if self.mask.get_at((x, y)):  
                                    color = self.image.get_at((x, y))
                                    dark_color = (max(color[0] - 50, 0), 
                                                  max(color[1] - 50, 0), 
                                                  max(color[2] - 50, 0), 
                                                  color[3])
                                    darken_image.set_at((x, y), dark_color)

                        self.image.blit(darken_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                        # Play button sound
                        button_sound.play()

                    # Set darken time
                    self.darken_start_time = pygame.time.get_ticks()

                    action = True
            
                elif pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                    self.clicked = False
                    self.reset_effects()

            # Check if darken effect duration has passed
            if self.darken_start_time:
                current_time = pygame.time.get_ticks()
                if current_time - self.darken_start_time >= self.darken_duration:
                    self.reset_effects()
                    self.darken_start_time = None  

        # Draw button on screen
        screen.blit(self.image, self.rect.topleft)
        
        return action
    
    def reset_effects(self):
        self.image = self.original_image.copy()
        center = self.rect.center  # Keep the current center position
        self.rect = self.image.get_rect(center=center)  #Restore original rect
    
