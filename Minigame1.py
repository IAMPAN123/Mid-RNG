# #WIP
import pygame

pygame.display.init()
pygame.mixer.init()

Score = 0
status = None
KeyPressed = False
Selected = 'white'
Unselected = 'gray'
ButtonStates = {True : Selected, False : Unselected}
#hitsound = pygame.mixer.Sound()


#music
spe = pygame.mixer.Sound('Audio/specialz.ogg')
spe.set_volume(0.5)

#dim
class sysui:
    @staticmethod
    def init(app):
        sysui.center = (app.screen.get_size()[0]//2, app.screen.get_size()[1]//2)
        sysui.half_width = app.screen.get_size()[0]//2
        sysui.half_height = app.screen.get_size()[1]//2

#beatmap
class printslider:
    def __init__(self, app, bg='black'):
        self.app = app
        self.bg = bg

        self.sliders = [slider((300,400), (200,60), 0.5, 0, 100), slider((300,600), (400,60), 0.5, 0, 100)]

    def run(self, slidernum):
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()

        self.app.fill("black")
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
        pygame.draw.rect(app, "darkgray", self.container_rect, 2, 26)
        pygame.draw.rect(app, ButtonStates[self.hovered], self.button_rect, 1, 26)

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos - (self.size[1]/2)
        button_val = self.button_rect.centerx - self.slider_left_pos
        return (button_val/val_range)*(self.max-self.min)+self.min
    
    def score(self):
        if self.get_value() == 100:
            return True

#mainloop
class minigame1:
    def __init__(self, screen):
        #pygame.init()
        #screen = pygame.display.set_mode((600,700))
        #sysui.init(screen)
        #pygame.display.set_caption("minigame1")
        #pygame.mouse.set_visible(False)
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.cursor = pygame.image.load('Images/cursor2.png').convert_alpha()
        self.cursor = pygame.transform.scale(self.cursor, (50,50))
        self.halfcursorwidth = self.cursor.get_width()/2
        self.halfcursorheight = self.cursor.get_height()/2
        self.ps = printslider(screen)
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

    def run(self, screen):
        global Score
        global KeyPressed
        global status
        spe.play()
        screenstate = 'cir1'
        self.running = True
        self.timer = pygame.time.get_ticks()
        while self.running:

            mousepos = pygame.mouse.get_pos()

            if screenstate == 'cir1':
                
                screen.fill('black')
                if self.cir1.draw(screen):
                    Score += 1
                    screenstate = 'cir2'

            if screenstate == 'cir2':
                screen.fill('black')
                if self.cir2.draw(screen):
                    Score += 1
                    screenstate = 'cir3'
            
            if screenstate == 'cir3':
                screen.fill('black')
                if self.cir3.draw(screen):
                    Score += 1
                    screenstate = 'slider1'

            if screenstate == 'slider1':
                screen.fill('black')
                if self.ps.run(0):
                    Score += 1
                    screenstate = 'cir4'

            if screenstate == 'cir4':
                screen.fill('black')
                if self.cir4.draw(screen):
                    Score += 1
                    screenstate = 'cir5'

            if screenstate == 'cir5':
                screen.fill('black')
                if self.cir5.draw(screen):
                    Score += 1
                    screenstate = 'cir6'

            if screenstate == 'cir6':
                screen.fill('black')
                if self.cir6.draw(screen):
                    Score += 1
                    screenstate = 'cir7'

            if screenstate == 'cir7':
                screen.fill('black')
                if self.cir7.draw(screen):
                    Score += 1
                    screenstate = 'cir8'

            if screenstate == 'cir8':
                screen.fill('black')
                if self.cir8.draw(screen):
                    Score += 1
                    screenstate = 'cir9'

            if screenstate == 'cir9':
                screen.fill('black')
                if self.cir9.draw(screen):
                    Score += 1
                    screenstate = 'cir10'

            if screenstate == 'cir10':
                screen.fill('black')
                if self.cir10.draw(screen):
                    Score += 1
                    screenstate = 'cir11'

            if screenstate == 'cir11':
                screen.fill('black')
                if self.cir11.draw(screen):
                    Score += 1
                    screenstate = 'cir12'

            if screenstate == 'cir12':
                screen.fill('black')
                if self.cir12.draw(screen):
                    Score += 1
                    screenstate = 'cir13'

            if screenstate == 'cir13':
                screen.fill('black')
                if self.cir13.draw(screen):
                    Score += 1
                    screenstate = 'cir14'

            if screenstate == 'cir14':
                screen.fill('black')
                if self.cir14.draw(screen):
                    Score += 1
                    screenstate = 'cir15'

            if screenstate == 'cir15':
                screen.fill('black')
                if self.cir15.draw(screen):
                    Score += 1
                    screenstate = 'cir16'

            if screenstate == 'cir16':
                screen.fill('black')
                if self.cir16.draw(screen):
                    Score += 1
                    screenstate = 'cir17'

            if screenstate == 'cir17':
                screen.fill('black')
                if self.cir17.draw(screen):
                    Score += 1
                    screenstate = 'cir18'

            if screenstate == 'cir18':
                screen.fill('black')
                if self.cir18.draw(screen):
                    Score += 1
                    screenstate = 'cir19'

            if screenstate == 'cir19':
                screen.fill('black')
                if self.cir19.draw(screen):
                    Score += 1
                    screenstate = 'cir20'

            if screenstate == 'cir20':
                screen.fill('black')
                if self.cir20.draw(screen):
                    Score += 1
                    screenstate = 'cir21'

            if screenstate == 'cir21':
                screen.fill('black')
                if self.cir21.draw(screen):
                    Score += 1
                    screenstate = 'cir22'

            if screenstate == 'cir22':
                screen.fill('black')
                if self.cir22.draw(screen):
                    Score += 1
                    screenstate = 'cir23'

            if screenstate == 'cir23':
                screen.fill('black')
                if self.cir23.draw(screen):
                    Score += 1
                    screenstate = 'cir24'

            if screenstate == 'cir24':
                screen.fill('black')
                if self.cir24.draw(screen):
                    Score += 1
                    screenstate = 'cir25'

            if screenstate == 'cir25':
                screen.fill('black')
                if self.cir25.draw(screen):
                    Score += 1
                    screenstate = 'slider2'

            if screenstate == 'slider2':
                screen.fill('black')
                if self.ps.run(1):
                    Score += 1
                    self.endtimer = pygame.time.get_ticks()
                    screenstate = 'blank'

            if screenstate == 'blank':
                screen.fill('black')
                print((self.endtimer - self.timer)//1000)
                try:
                    if self.endtimer - self.timer < 11000:
                        status = 'Fail'
                    elif self.endtimer - self.timer > 13000:
                        status = 'Fail'
                    else:
                        status = 'Pass'
                finally:
                    spe.stop()
                    self.running = False

            screen.blit(self.cursor, (mousepos[0] - self.halfcursorheight, mousepos[1] - self.halfcursorwidth))

            #event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    spe.stop()
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    KeyPressed = True
                if event.type == pygame.KEYUP:
                    KeyPressed = False

            #print(Score)
            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(60)

        #pygame.quit()
    
#game = minigame1()
#game.run()