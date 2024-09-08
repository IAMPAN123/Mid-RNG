#WIP
import pygame

pygame.display.init()
pygame.mixer.init()

Score = 0
Selected = 'white'
Unselected = 'gray'
ButtonStates = {True : Selected, False : Unselected}
#hitsound = pygame.mixer.Sound()


#dim
class sysui:
    @staticmethod
    def init(app):
        sysui.center = (app.scrn.get_size()[0]//2, app.scrn.get_size()[1]//2)
        sysui.half_width = app.scrn.get_size()[0]//2
        sysui.half_height = app.scrn.get_size()[1]//2

#beatmap
class printslider:
    def __init__(self, app, bg='black'):
        self.app = app
        self.bg = bg

        self.sliders = [slider(sysui.center, (200,60), 0.5, 0, 100)]

    def run(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()

        self.app.scrn.fill("black")
        for slider in self.sliders:
            if slider.button_rect.collidepoint(mouse_pos):
                if mouse[0]:
                    slider.grabbed = True
            if not mouse[0]:
                slider.grabbed = False
            if slider.button_rect.collidepoint(mouse_pos):  
                slider.hover()
            if slider.grabbed:
                slider.moveslider(mouse_pos)
                slider.hover()
            else:
                slider.hovered = False
            slider.render(self.app)
            slider.score()

#Score

#circle (straight from huisze)
class Circle():
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

    #draw img
    def draw(self, screen):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos)and self.mask.get_at((pos[0] - self.rect.x, pos[1] - self.rect.y)):

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
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
                            #darken opaque area
                            if self.mask.get_at((x, y)):  
                                color = self.image.get_at((x, y))
                                dark_color = (max(color[0] - 50, 0), 
                                              max(color[1] - 50, 0), 
                                              max(color[2] - 50, 0), 
                                              color[3])
                                darken_image.set_at((x, y), dark_color)

                    self.image.blit(darken_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                     #play button sound
                    #hitsound.play()

                #set darken time
                self.darken_start_time = pygame.time.get_ticks()

                action = True
        
            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                self.reset_effects()

         # Check if darken effect duration has passed
        if self.darken_start_time:
            current_time = pygame.time.get_ticks()
            if current_time - self.darken_start_time >= self.darken_duration:
                self.reset_effects()
                self.darken_start_time = None  

		#draw button on screen
        screen.blit(self.image, self.rect.topleft)
        
        return action
    
    def reset_effects(self):
        self.image = self.original_image.copy()
        center = self.rect.center  # Keep the current center position
        self.rect = self.image.get_rect(center=center)  #Restore original rect

#slider
class slider:
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min: int, max: int):
        self.pos = pos
        self.size = size
        self.hovered = False
        self.grabbed = False

        self.slider_left_pos = self.pos[0] - (size[0]//2)
        self.slider_right_pos = self.pos[0] + (size[0]//2)
        self.slider_top_pos = self.pos[1] - (size[1]//2)

        self.min = min
        self.max = max
        self.initial_val = (self.slider_right_pos-self.slider_left_pos)*initial_val # <- percentage

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[1], self.size[1])

    def moveslider(self, mouse_pos):
        pos = mouse_pos[0]
        if pos < self.slider_left_pos + (self.size[1]/2):
            pos = self.slider_left_pos + (self.size[1]/2)
        if pos > self.slider_right_pos - (self.size[1]/2):
            pos = self.slider_right_pos - (self.size[1]/2)
        self.button_rect.centerx = pos

    def hover(self):
        self.hovered = True

    def render(self, app):
        pygame.draw.rect(app.scrn, "darkgray", self.container_rect, 2, 26)
        pygame.draw.rect(app.scrn, ButtonStates[self.hovered], self.button_rect, 1, 26)

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos - (self.size[1]/2)
        button_val = self.button_rect.centerx - self.slider_left_pos
        return (button_val/val_range)*(self.max-self.min)+self.min
    
    def score(self):
        if self.get_value() == 100:
            global Score
            Score += 1
            print(Score)

def RemoveButton():
    width = 600
    height = 700
    scrn = pygame.display.set_mode((width, height))
    bg = pygame.Surface(scrn.get_size())
    bg = bg.convert()
    bg.fill('black')
    scrn.blit(bg, (0, 0))
    pygame.display.flip()

def ButtonClicked(button, scrn):
    if button.draw(scrn):
        return True
    else:
        return False

#mainloop
class minigame1:
    def __init__(self):
        pygame.init()
        self.scrn = pygame.display.set_mode((600,700))
        sysui.init(self)
        pygame.display.set_caption("minigame1")
        pygame.mouse.set_visible(False)
        self.cursor = pygame.image.load('Images/cursor.png').convert_alpha()
        self.cursor = pygame.transform.scale(self.cursor, (50,50))
        self.halfcursorwidth = self.cursor.get_width()/2
        self.halfcursorheight = self.cursor.get_height()/2
        self.ps = printslider(self)
        self.testupgimg = pygame.image.load('Images/placeholder.png').convert_alpha()
        self.testupg = Circle(500, 50, self.testupgimg, width = 50, height = 50)

    def run(self):
        self.running = True
        while self.running:
            self.scrn.fill('black')
            
            mousepos = pygame.mouse.get_pos()

            self.ps.run()

            if ButtonClicked(self.testupg, self.scrn):
                RemoveButton()

            self.scrn.blit(self.cursor, (mousepos[0] - self.halfcursorheight, mousepos[1] - self.halfcursorwidth))

            #event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.update()

        pygame.quit()
    
game = minigame1()
game.run()