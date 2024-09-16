#WIP
import pygame

pygame.display.init()
pygame.mixer.init()

Score = 0
KeyPressed = False
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

        self.sliders = [slider(sysui.center, (200,60), 0.5, 0, 100), slider((300,600), (400,60), 0.5, 0, 100)]

    def run(self, slidernum):
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()

        self.app.scrn.fill("black")
        slider = self.sliders[slidernum]
        if slider.button_rect.collidepoint(mouse_pos):
            if mouse[0] or KeyPressed:
                slider.grabbed = True
        if not (mouse[0] or KeyPressed):
            slider.grabbed = False
        if slider.button_rect.collidepoint(mouse_pos):  
            slider.hover()
        if slider.grabbed:
            slider.moveslider(mouse_pos)
            slider.hover()
        else:
            slider.hovered = False
        slider.render(self.app)
        return slider.score()
        

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

            if (pygame.mouse.get_pressed()[0] == 1 or KeyPressed == True) and self.clicked == False:
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
        
            elif (pygame.mouse.get_pressed()[0] == 0 or KeyPressed == False) and self.clicked == True:
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
            return True

#mainloop
class minigame1:
    def __init__(self):
        pygame.init()
        self.scrn = pygame.display.set_mode((600,700))
        sysui.init(self)
        pygame.display.set_caption("minigame1")
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.cursor = pygame.image.load('Images/cursor.png').convert_alpha()
        self.cursor = pygame.transform.scale(self.cursor, (50,50))
        self.halfcursorwidth = self.cursor.get_width()/2
        self.halfcursorheight = self.cursor.get_height()/2
        self.ps = printslider(self)
        self.circleimg = pygame.image.load('Images/hitcircle.png').convert_alpha()
        self.cir1 = Circle(470, 75, self.circleimg, width = 50, height = 50)
        self.cir2 = Circle(520, 110, self.circleimg, width = 50, height = 50)
        self.cir3 = Circle(450, 170, self.circleimg, width = 50, height = 50)
        self.cir4 = Circle(460, 200, self.circleimg, width = 50, height = 50)
        self.cir5 = Circle(410, 165, self.circleimg, width = 50, height = 50)
        self.cir6 = Circle(320, 190, self.circleimg, width = 50, height = 50)
        self.cir7 = Circle(210, 190, self.circleimg, width = 50, height = 50)
        self.cir8 = Circle(370, 210, self.circleimg, width = 50, height = 50)
        self.cir9 = Circle(320, 300, self.circleimg, width = 50, height = 50)
        self.cir10 = Circle(370, 210, self.circleimg, width = 50, height = 50)
        self.cir11 = Circle(460, 210, self.circleimg, width = 50, height = 50)
        self.cir12 = Circle(320, 200, self.circleimg, width = 50, height = 50)
        self.cir13 = Circle(210, 200, self.circleimg, width = 50, height = 50)
        self.cir14 = Circle(370, 220, self.circleimg, width = 50, height = 50)
        self.cir15 = Circle(320, 310, self.circleimg, width = 50, height = 50)
        self.cir16 = Circle(370, 220, self.circleimg, width = 50, height = 50)
        self.cir17 = Circle(460, 220, self.circleimg, width = 50, height = 50)
        self.cir18 = Circle(320, 210, self.circleimg, width = 50, height = 50)
        self.cir19 = Circle(210, 210, self.circleimg, width = 50, height = 50)
        self.cir20 = Circle(370, 230, self.circleimg, width = 50, height = 50)
        self.cir21 = Circle(320, 320, self.circleimg, width = 50, height = 50)
        self.cir22 = Circle(370, 230, self.circleimg, width = 50, height = 50)
        self.cir23 = Circle(520, 110, self.circleimg, width = 50, height = 50)
        self.cir24 = Circle(210, 300, self.circleimg, width = 50, height = 50)
        self.cir25 = Circle(520, 500, self.circleimg, width = 50, height = 50)
        self.timer = pygame.time.get_ticks()

    def run(self):
        global Score
        global KeyPressed
        self.scrnstate = 'cir1'
        self.running = True
        while self.running:

            mousepos = pygame.mouse.get_pos()

            if self.scrnstate == 'cir1':
                self.scrn.fill('black')
                if self.cir1.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir2'

            if self.scrnstate == 'cir2':
                self.scrn.fill('black')
                if self.cir2.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir3'
            
            if self.scrnstate == 'cir3':
                self.scrn.fill('black')
                if self.cir3.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'slider1'

            if self.scrnstate == 'slider1':
                self.scrn.fill('black')
                if self.ps.run(0):
                    Score += 1
                    self.scrnstate = 'cir4'

            if self.scrnstate == 'cir4':
                self.scrn.fill('black')
                if self.cir4.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir5'

            if self.scrnstate == 'cir5':
                self.scrn.fill('black')
                if self.cir5.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir6'

            if self.scrnstate == 'cir6':
                self.scrn.fill('black')
                if self.cir6.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir7'

            if self.scrnstate == 'cir7':
                self.scrn.fill('black')
                if self.cir7.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir8'

            if self.scrnstate == 'cir8':
                self.scrn.fill('black')
                if self.cir8.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir9'

            if self.scrnstate == 'cir9':
                self.scrn.fill('black')
                if self.cir9.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir10'

            if self.scrnstate == 'cir10':
                self.scrn.fill('black')
                if self.cir10.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir11'

            if self.scrnstate == 'cir11':
                self.scrn.fill('black')
                if self.cir11.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir12'

            if self.scrnstate == 'cir12':
                self.scrn.fill('black')
                if self.cir12.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir13'

            if self.scrnstate == 'cir13':
                self.scrn.fill('black')
                if self.cir13.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir14'

            if self.scrnstate == 'cir14':
                self.scrn.fill('black')
                if self.cir14.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir15'

            if self.scrnstate == 'cir15':
                self.scrn.fill('black')
                if self.cir15.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir16'

            if self.scrnstate == 'cir16':
                self.scrn.fill('black')
                if self.cir16.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir17'

            if self.scrnstate == 'cir17':
                self.scrn.fill('black')
                if self.cir17.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir18'

            if self.scrnstate == 'cir18':
                self.scrn.fill('black')
                if self.cir18.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir19'

            if self.scrnstate == 'cir19':
                self.scrn.fill('black')
                if self.cir19.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir20'

            if self.scrnstate == 'cir20':
                self.scrn.fill('black')
                if self.cir20.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir21'

            if self.scrnstate == 'cir21':
                self.scrn.fill('black')
                if self.cir21.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir22'

            if self.scrnstate == 'cir22':
                self.scrn.fill('black')
                if self.cir22.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir23'

            if self.scrnstate == 'cir23':
                self.scrn.fill('black')
                if self.cir23.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir24'

            if self.scrnstate == 'cir24':
                self.scrn.fill('black')
                if self.cir24.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'cir25'

            if self.scrnstate == 'cir25':
                self.scrn.fill('black')
                if self.cir25.draw(self.scrn):
                    Score += 1
                    self.scrnstate = 'slider2'

            if self.scrnstate == 'slider2':
                self.scrn.fill('black')
                if self.ps.run(1):
                    Score += 1
                    self.endtimer = pygame.time.get_ticks()
                    self.scrnstate = 'blank'

            if self.scrnstate == 'blank':
                self.scrn.fill('black')
                print((self.endtimer - self.timer)//1000)
                try:
                    if self.endtimer - self.timer < 9000:
                        print('Fail (Too early)')
                    elif self.endtimer - self.timer > 11000:
                        print('Fail (Too late)')
                    else:
                        print('Pass')
                finally:
                    self.running = False

            self.scrn.blit(self.cursor, (mousepos[0] - self.halfcursorheight, mousepos[1] - self.halfcursorwidth))

            #event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    KeyPressed = True
                if event.type == pygame.KEYUP:
                    KeyPressed = False

            #print(Score)
            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
    
game = minigame1()
game.run()