import pygame

pygame.mixer.init()

#load sound
button_sound = pygame.mixer.Sound("clicks.mp3")

#Define
class Button():
    #load img
    def __init__(self, x, y, image, width=None, height=None):
        if width and height:
            self.original_image = pygame.transform.scale(image,(width, height))
        else:
            self.original_image = image
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    #draw img
    def draw(self, screen):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True

                # Button press effect
                self.image = pygame.transform.scale(self.original_image, 
                                (int(self.rect.width * 0.95), int(self.rect.height * 0.95)))
                darken_image = pygame.Surface(self.image.get_size()).convert_alpha()
                darken_image.fill((0, 0, 0, 50))  # 50 is the alpha value
                self.image.blit(darken_image, (0, 0))

                #play button sound
                button_sound.play()

                # Delay
                pygame.time.delay(120) 

                action = True
        
            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                self.image = self.original_image

		#draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        return action
    
    def reset(self):
        self.clicked = False
        self.image = self.original_image
