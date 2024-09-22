import pygame
import random
import CurrencyAndUpgrades as cu
import SliderExample as cd
from button import Button
from Game.inventory import Inventory
from Game.gui import draw_inventory  # Check that draw_inventory is not conflicting with inventory.draw
from Game.equipment import Equipment
from roll_animation import Animation

import json
# Load item-to-slot mapping from JSON
with open('Game/item_to_slot_count.json', 'r') as file:
    item_to_slot_count = json.load(file)
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((600, 700))
pygame.font.init()
pygame.display.set_caption("RNG")

import Rolling as r

# Load background music
pygame.mixer.music.load('Audio/bgm.mp3')
pygame.mixer.music.play(-1)

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
testupgimg = pygame.image.load("Images/placeholder.png").convert_alpha()
equipment_img = pygame.image.load('Images/equipment.png').convert_alpha()
return_img = pygame.image.load("Images/return.png").convert_alpha()
mute_img = pygame.image.load("Images/mute.png").convert_alpha()
open_img = pygame.image.load("Images/opsound.png").convert_alpha()
increase_img = pygame.image.load("Images/icsound.png").convert_alpha()
decrease_img = pygame.image.load("Images/dcsound.png").convert_alpha()


# Create button instances
start_button = Button(300, 450, start_img, width = 450, height = 302)
exit_button = Button(0, 0, exit_img, width = 250, height = 94, effect_enabled = False)
backpack_button = Button(100, 600, backpack_img, width= 100 , height= 95)
roll_button = Button(300, 600, roll_img, width = 249, height = 95)
setting_button = Button(500, 600, setting_img, width = 100, height = 95)
instructions_button = Button(0, 0, instructions_img, width = 250, height = 96, effect_enabled = False)
cross_button = Button(0, 0, cross_img, width = 90, height = 85, effect_enabled = False)
testupg = Button(500, 50, testupgimg, width = 100, height = 50)
equipment_button = Button(100, 450, equipment_img, width=100, height=95)  # Positioned above the inventory button
return_button = Button(0, 0, return_img, width = 75, height = 75, effect_enabled = False)
mute_button = Button(0, 0, mute_img, width = 72, height = 76)
open_button = Button(0, 0, open_img, width = 75, height = 82)
ic_button = Button(0, 0, increase_img, width = 70, height = 79)
dc_button = Button(0, 0, decrease_img, width = 75, height = 75)

# Define initial volume
volume = 0.5  
pygame.mixer.music.set_volume(volume)

# Define animation paths
common_paths = [f'Images/common pic/common_br_{i:03}.png' for i in range(34)]
uncommon_paths = [f'Images/uncommon pic/uncommon_br_{i:03}.png' for i in range(34)]
rare_paths = [f'Images/rare pic/rare_br_{i:03}.png' for i in range(34)]
epic_paths = [f'Images/epic pic/epic_br_{i:03}.png' for i in range(33)]
legendary_paths = [f'Images/legendary pic/legendary_br_{i:03}.png' for i in range(33)]
mythic_paths = [f'Images/mythic pic/mythic_{i:03}.png' for i in range(33)]
fraud_paths = [f'Images/fraud pic/fraud_{i:03}.png' for i in range(32)]
worm_paths = [f'Images/worm pic/worm_{i:03}.png' for i in range(33)]
judge_paths = [f'Images/judge pic/judge_{i:03}.png' for i in range(33)]
gambler_paths = [f'Images/gambler pic/gambler_{i:03}.png' for i in range(32)]
baby_paths = [f'Images/baby pic/baby_{i:03}.png' for i in range(33)]
comedian_paths = [f'Images/comedian pic/comedian_{i:03}.png' for i in range(33)]
farmer_paths = [f'Images/farmer pic/farmer_{i:03}.png' for i in range(32)]
cat_paths = [f'Images/cat pic/cat_{i:03}.png' for i in range(32)]
freaky_paths = [f'Images/freaky pic/freaky_{i:03}.png' for i in range(32)]
misogynint_paths = [f'Images/misogynint pic/misogynint_{i:03}.png' for i in range(32)]
specialz_paths = [f'Images/specialz pic/specialz_{i:03}.png' for i in range(32)]
nah_paths = [f'Images/nah pic/nah_{i:03}.png' for i in range(32)]
void_paths = [f'Images/void pic/void_{i:03}.png' for i in range(33)]
malevolent_paths = [f'Images/malevolent pic/malevolent_{i:03}.png' for i in range(33)]

# Create animation instances
animations = {
    'Common': Animation(common_paths, (450, 253), (75, 75)),
    'Uncommon': Animation(uncommon_paths, (450, 253), (75, 75)),
    'Rare': Animation(rare_paths, (450, 253), (75, 75)),
    'Epic': Animation(epic_paths, (450, 253), (75, 75)),
    'Legendary': Animation(legendary_paths, (450, 253), (75, 75)),
    'Mythic':  Animation(legendary_paths, (450, 253), (75, 75)),
    'Fraud':  Animation(legendary_paths, (450, 253), (75, 75)),
    'Worm':  Animation(legendary_paths, (450, 253), (75, 75)),
    'Judge':  Animation(legendary_paths, (450, 253), (75, 75)),
    'Gambler':  Animation(legendary_paths, (450, 253), (75, 75)),
    'Baby':  Animation(legendary_paths, (450, 253), (75, 75)),
    'Comedian':  Animation(legendary_paths, (450, 253), (75, 75)),
    'Farmer':  Animation(legendary_paths, (450, 253), (75, 75)),
    'Cat':  Animation(legendary_paths, (450, 253), (75, 75)),
    'Freaky':  Animation(legendary_paths, (450, 253), (75, 75)),
    'Misogynint':  Animation(legendary_paths, (450, 253), (75, 75)),
    'Specialz':  Animation(legendary_paths, (450, 253), (75, 75)),
    'Nah':  Animation(legendary_paths, (450, 253), (75, 75)),
    'Void':  Animation(legendary_paths, (450, 253), (75, 75)),
    'Malevolent':  Animation(legendary_paths, (450, 253), (75, 75)),
}

# Initialize inventory and equipment
inventory = Inventory(screen)
equipment = Equipment(screen) 

# Panel state
settings_active = False
instruction_active = False
current_animation = None

# Load custom mouse cursor image
cursor_image = pygame.transform.scale(pygame.image.load('Images/cursor.png').convert_alpha(), (40, 39))
pygame.mouse.set_visible(False)  # Hide default mouse cursor

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
                    
                    # Increment the counter for the rolled item
                    if x in item_to_slot_count:
                        inventory.increment_counter(x)
                        inventory.save_item_counts()

                     # Set the animation based on rarity
                    current_animation = animations[x]
                    current_animation.reset()

                    break
                else:
                    continue
            except ValueError:
                None

def setting():
    global settings_active,instruction_active, volume
    if instruction_active:
        instruction()
    else:
        # Draw setting panel
        panel_rect = pygame.Rect(100, 150, 400, 400)
        pygame.draw.rect(screen, (211, 211, 211), panel_rect)

        # Button position
        cross_button.rect.center = (panel_rect.x + 355, panel_rect.y + 45)
        instructions_button.rect.center = (panel_rect.x + 200, panel_rect.y + 200)
        exit_button.rect.center = (panel_rect.x + 200, panel_rect.y + 320)
        mute_button.rect.center = (panel_rect.x + 230, panel_rect.y + 105)
        open_button.rect.center = (panel_rect.x + 295, panel_rect.y + 105)
        ic_button.rect.center = (panel_rect.x + 165, panel_rect.y + 107)
        dc_button.rect.center = (panel_rect.x + 100, panel_rect.y + 100)

        if cross_button.draw(screen):
            settings_active = False
        if instructions_button.draw(screen):
            instruction_active = True
        if exit_button.draw(screen):
            pygame.quit()
            exit()

        if mute_button.draw(screen):
            volume = 0 
            pygame.mixer.music.set_volume(volume)
        if open_button.draw(screen):
            volume = 0.5
            pygame.mixer.music.set_volume(volume)
        if ic_button.draw(screen):
            volume = min(1.0, volume + 0.1)
            pygame.mixer.music.set_volume(volume)
        if dc_button.draw(screen):
            volume = max(0.0, volume - 0.1)
            pygame.mixer.music.set_volume(volume)
        
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
        text_surface = font.render(line, True, (0, 0, 0)) 
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

def update():
    # Check if inventory is open and draw the inventory if it is
    if inventory.is_open:
        inventory.update_animation()  # Call this to update any ongoing animations
        inventory.draw()  # Ensure inventory is drawn when open

    # Equipment screen handling
    if equipment.is_open:
        equipment.draw()  # Draw equipment screen

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
        
        if equipment_button.draw(screen):
            equipment.open()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if inventory.is_open:  # Only handle inventory events if it's open
                inventory.handle_event(event)
            if equipment.is_open:
                equipment.handle_event(event)

        if roll_button.draw(screen):
            roll()
        if setting_button.draw(screen):
            settings_active = True
        if testupg.draw(screen):
            cu.totalupg += 1
            cu.testupg += 1
            cu.passivegain += 1

        update()
            
    # Update and draw the current animation
    if current_animation:
        current_animation.update()
        current_animation.draw(screen)
        if current_animation.finished:
            current_animation = None

        update()

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

    # Draw custom mouse cursor
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.blit(cursor_image, (mouse_x, mouse_y))

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inventory.save_item_counts()
            running = False        

    pygame.display.update()
    clock.tick(60)

pygame.quit()
