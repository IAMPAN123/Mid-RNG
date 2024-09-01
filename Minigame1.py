#WIP
import pygame

#cursor
class cursorclass:
    def __init__(self):
        self.cursor = pygame.image.load('Images/cursor.png').convert_alpha()
        self.cursor = pygame.transform.scale(self.cursor, (50,50))

    def run(self):
        mousepos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()

#slider
class slider:
    def __init__(self):
        pass

    def run(self):
        pass

#mainloop
class minigame1:
    def __init__(self):
        pygame.init()
        self.scrn = pygame.display.set_mode((600,700))
        pygame.display.set_caption("minigame1")
        pygame.mouse.set_visible(False)
        self.cursor = pygame.image.load('Images/cursor.png').convert_alpha()
        self.cursor = pygame.transform.scale(self.cursor, (50,50))

    def run(self):
        self.running = True
        while self.running:
            self.scrn.fill('black')
            
            mousepos = pygame.mouse.get_pos()
            self.scrn.blit(self.cursor, mousepos)

            #event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.update()

        pygame.quit()
    
game = minigame1()
game.run()