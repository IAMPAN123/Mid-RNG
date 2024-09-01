import pygame
import random
import Rolling as r
import Currency as c
from button import Button
from Game.inventory import Inventory
from Game.roll import roll
from Game.gui import draw_inventory

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((600, 700))
pygame.display.set_caption("RNG")

#set up text and font
mfont = pygame.font.SysFont("Comic Sans MS", 30)
gdisplay = mfont.render(f'Gold = {c.gold}', False, (250, 250, 250))

#set up bg
bg1 = pygame.image.load("Images/bg.png")
bg1 = pygame.transform.scale(bg1,(600,700))

#set up title
title = pygame.image.load("Images/title.png").convert_alpha()

#adjust size
title_img = pygame.transform.scale(title, (250, 148)) 

title_rect = title.get_rect()
title_rect.center = (300, 150)

#set up button
start_img = pygame.image.load("Images/start.png").convert_alpha()
exit_img = pygame.image.load("Images/exit.png").convert_alpha()
backpack_img = pygame.image.load("Images/bp.png").convert_alpha()
roll_img = pygame.image.load("Images/roll.png").convert_alpha()
setting_img = pygame.image.load("Images/st.png").convert_alpha()
instructions_img = pygame.image.load("Images/instructions.png").convert_alpha()
cross_img = pygame.image.load("Images/cross.png").convert_alpha()


#create button instances
start_button = Button(300, 450, start_img, width = 450, height = 302)
exit_button = Button(0, 0, exit_img, width = 300, height = 113, effect_enabled = False)
backpack_button = Button(100, 600, backpack_img, width= 100 , height= 95)
roll_button = Button(300, 600, roll_img, width = 249, height = 95)
setting_button = Button(500, 600, setting_img, width = 100, height = 95)
instructions_button = Button(0, 0, instructions_img, width = 300, height = 115, effect_enabled = False)
cross_button = Button(0, 0, cross_img, width = 100, height = 95, effect_enabled = False)

# Initialize inventory
inventory = Inventory(screen)

#panel state
settings_active = False

def roll():
    for x in r.Rarity:
            NotActualFinalChance = (r.FinalChance(1/(r.Rarity[x]), r.Luck, r.Bonus))
            ActualFinalChance = 1/NotActualFinalChance
            try:
                Result = random.randint(1, int(ActualFinalChance))
                if Result == 1:
                    print(x)
                    c.gaingold(r.Rarity[x])
                    r.BonusRollCount += 1
                    if r.BonusRollCount == 10:
                        r.Bonus = 2
                    elif r.BonusRollCount > 10:
                        r.Bonus = 1
                    break
                else:
                    continue
            except ValueError:
                None

def setting():
    global settings_active
    #draw panel
    panel_rect = pygame.Rect(100, 150, 400, 400)
    pygame.draw.rect(screen, (211, 211, 211), panel_rect)
    #button position
    cross_button.rect.center = (panel_rect.x + 350, panel_rect.y + 50)
    instructions_button.rect.center = (panel_rect.x + 200, panel_rect.y + 150)
    exit_button.rect.center = (panel_rect.x + 200, panel_rect.y + 300)

    if cross_button.draw(screen):
       return True
    if instructions_button.draw(screen):
        print("Show instructions")
    if exit_button.draw(screen):
        pygame.quit()
        exit()

    return False

def fade_out(width, height):
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))

    for alpha in range (0, 255):
        fade.set_alpha(alpha)
        screen.blit(fade,(0,0))
        pygame.display.update()
        pygame.time.delay(4)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.blit(bg1, (0, 0))

    if inventory.current_page == 1:
        screen.blit(title, title_rect)
        if start_button.draw(screen):
            fade_out(600,700)
            inventory.current_page = 2
        
    elif inventory.current_page == 2:
        screen.fill((0,0,0))
        screen.blit(gdisplay, (10, 0))

        if backpack_button.draw(screen):
            inventory.open()
        if roll_button.draw(screen):
            roll()
        if setting_button.draw(screen):
            settings_active = True
        if inventory.is_open:
            draw_inventory(screen, inventory)

    if settings_active:
        #overlay main screen
        overlay = pygame.Surface(screen.get_size())
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150) 
        screen.blit(overlay, (0, 0))
       
        if setting():
            settings_active = False

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        inventory.handle_event(event)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
