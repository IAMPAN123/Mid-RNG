import pygame

#Define
class Button():
    #load img
    def __init__(self, x, y, image, width=None, height=None):
        if width and height:
            self.image = pygame.transform.scale(image,(width, height))
        else:
            self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
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
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

		#draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        return action
