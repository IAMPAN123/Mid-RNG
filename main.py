import pygame
import random
import Rolling as r
import CurrencyAndUpgrades as cu
import SliderExample as cd
from button import Button
from Game.inventory import Inventory
from Game.roll import roll
from Game.gui import draw_inventory  # Check that draw_inventory is not conflicting with inventory.draw
from roll_animation import Animation

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((600, 700))
pygame.display.set_caption("RNG")

# Set up text and font
mfont = pygame.font.SysFont("Comic Sans MS", 30)
gdisplay = mfont.render(f'Gold = {cu.gold}', False, (250, 250, 250))

# Set up background
bg1 = pygame.image.load("Images/bg.png")
bg1 = pygame.transform.scale(bg1, (600, 700))

# Set up title
title = pygame.image.load("Images/title.png").convert_alpha()
title_img = pygame.transform.scale(title, (250, 148)) 
title_rect = title.get_rect()
title_rect.center = (300, 150)

# Set up buttons
start_img = pygame.image.load("Images/start.png").convert_alpha()
exit_img = pygame.image.load("Images/exit.png").convert_alpha()
backpack_img = pygame.image.load("Images/bp.png").convert_alpha()
roll_img = pygame.image.load("Images/roll.png").convert_alpha()
setting_img = pygame.image.load("Images/st.png").convert_alpha()
instructions_img = pygame.image.load("Images/instructions.png").convert_alpha()
cross_img = pygame.image.load("Images/cross.png").convert_alpha()
testupgimg = pygame.image.load('Images/placeholder.png').convert_alpha()
return_img = pygame.image.load('Images/return.png').convert_alpha()

# Create button instances
start_button = Button(300, 450, start_img, width = 450, height = 302)
exit_button = Button(0, 0, exit_img, width = 300, height = 113, effect_enabled = False)
backpack_button = Button(100, 600, backpack_img, width= 100 , height= 95)
roll_button = Button(300, 600, roll_img, width = 249, height = 95)
setting_button = Button(500, 600, setting_img, width = 100, height = 95)
instructions_button = Button(0, 0, instructions_img, width = 300, height = 115, effect_enabled = False)
cross_button = Button(0, 0, cross_img, width = 100, height = 95, effect_enabled = False)
testupg = Button(500, 50, testupgimg, width = 100, height = 50)
return_button = Button(0, 0, return_img, width = 75, height = 75, effect_enabled = False)

# Define animation paths
common_paths = [f'Images/common pic/common_br_{i:03}.png' for i in range(34)]
uncommon_paths = [f'Images/uncommon pic/uncommon_br_{i:03}.png' for i in range(34)]
rare_paths = [f'Images/rare pic/rare_br_{i:03}.png' for i in range(34)]
epic_paths = [f'Images/epic pic/epic_br_{i:03}.png' for i in range(33)]
legendary_paths = [f'Images/legendary pic/legendary_br_{i:03}.png' for i in range(33)]
mid_paths = [f'Images/mid pic/mid_br_{i:03}.png' for i in range(34)]

# Create animation instances
animations = {
    'Common': Animation(common_paths, (450, 300), (75, 150)),
    'Uncommon': Animation(uncommon_paths, (450, 300), (75, 150)),
    'Rare': Animation(rare_paths, (450, 300), (75, 150)),
    'Epic': Animation(epic_paths, (450, 300), (75, 150)),
    'Legendary': Animation(legendary_paths, (450, 300), (75, 150)),
    'Mid': Animation(mid_paths, (450, 290), (75, 140)),
}

# Initialize inventory
inventory = Inventory(screen)

# Panel state
settings_active = False
instruction_active = False
current_animation = None

def roll():
    global current_animation
    for x in r.Rarity:
            NotActualFinalChance = (r.FinalChance(1/(r.Rarity[x]), r.Luck, r.Bonus))
            ActualFinalChance = 1/NotActualFinalChance
            try:
                Result = random.randint(1, int(ActualFinalChance))
                if Result == 1:
                    print(x)
                    cu.gaingold(r.Rarity[x])
                    r.BonusRollCount += 1
                    if r.BonusRollCount == 10:
                        r.Bonus = 2
                    elif r.BonusRollCount > 10:
                        r.Bonus = 1

                     # Set the animation based on rarity
                    if x == 'Common':
                        current_animation = animations['Common']
                        current_animation.reset()
                    elif x == 'Uncommon':
                        current_animation = animations['Uncommon']
                        current_animation.reset()
                    elif x == 'Rare':
                        current_animation = animations['Rare']
                        current_animation.reset()
                    elif x == 'Epic':
                        current_animation = animations['Epic']
                        current_animation.reset()
                    elif x == 'Legendary':
                        current_animation = animations['Legendary']
                        current_animation.reset()
                    elif x == 'Mid':
                        current_animation = animations['Mid']
                        current_animation.reset()

                    break
                else:
                    continue
            except ValueError:
                None

def setting():
    global settings_active,instruction_active
    if instruction_active:
        instruction()
    else:
        # Draw setting panel
        panel_rect = pygame.Rect(100, 150, 400, 400)
        pygame.draw.rect(screen, (211, 211, 211), panel_rect)

        # Button position
        cross_button.rect.center = (panel_rect.x + 350, panel_rect.y + 50)
        instructions_button.rect.center = (panel_rect.x + 200, panel_rect.y + 150)
        exit_button.rect.center = (panel_rect.x + 200, panel_rect.y + 300)

        if cross_button.draw(screen):
            settings_active = False
        if instructions_button.draw(screen):
            instruction_active = True
        if exit_button.draw(screen):
            pygame.quit()
            exit()
    return False

def instruction():
    global instruction_active
    # Draw  instruction panel
    panel_rect = pygame.Rect(70, 100, 450, 450)
    pygame.draw.rect(screen, (255, 255, 255), panel_rect)

    # Set font
    font = pygame.font.SysFont("Comic Sans MS", 20)
    instruction_text = [
        "Welcome to the RNG Game!",
        "1. Roll to get random items.",
        "2. Upgrade your skills to earn more gold.",
        "3. Manage your inventory wisely."
    ]
    
    # Draw
    for i, line in enumerate(instruction_text):
        text_surface = font.render(line, True, (0, 0, 0))  # 黑色文本
        screen.blit(text_surface, (panel_rect.x + 20, panel_rect.y + 20 + i * 40))

    return_button.rect.center = (panel_rect.x + 400, panel_rect.y + 400)
    if return_button.draw(screen):
        instruction_active = False
        return False

    return True

def fade_out(width, height):
    fade = pygame.Surface((width, height))
    fade.fill((0, 0, 0))

    for alpha in range(0, 255):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(4)

def updategold():
    screen.fill((0, 0, 0))
    screen.blit(gdisplay, (10, 0))

# Main loop
running = True
clock = pygame.time.Clock()
LastTimeUpdate = pygame.time.get_ticks()

while running:
    screen.blit(bg1, (0, 0))

    if inventory.current_page == 1:
        screen.blit(title, title_rect)
        if start_button.draw(screen):
            fade_out(600, 700)
            inventory.current_page = 2
        
    elif inventory.current_page == 2:
        screen.fill((0, 0, 0))
        gdisplay = mfont.render(f'Gold = {cu.gold}', False, (250, 250, 250))
        screen.blit(gdisplay, (10, 0))

        if backpack_button.draw(screen):
            inventory.open()
        if roll_button.draw(screen):
            roll()
        if setting_button.draw(screen):
            settings_active = True
        if testupg.draw(screen):
            cu.totalupg += 1
            cu.testupg += 1
            cu.passivegain += 1

        # Check if inventory is open and draw the inventory if it is
        if inventory.is_open:
            inventory.update_animation()  # Call this every frame to update animation
            inventory.draw()  # Call the draw method for the inventory

    # Update and draw the current animation
    if current_animation:
        current_animation.update()
        current_animation.draw(screen)
        if current_animation.finished:
            current_animation = None

    if settings_active:
        # Overlay main screen
        overlay = pygame.Surface(screen.get_size())
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150) 
        screen.blit(overlay, (0, 0))
       
        if setting():
            settings_active = False

    CurrentTime = pygame.time.get_ticks()
    if cu.totalupg > 0 and CurrentTime - LastTimeUpdate >= 1000:
        cu.gold += cu.passivegain
        LastTimeUpdate = CurrentTime

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        inventory.handle_event(event)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
