import pygame
import random
import sys
import CurrencyAndUpgrades as cu
import Minigame1 as mini
from button import Button
from Game.inventory import Inventory
from Game.gui import draw_inventory  # Check that draw_inventory is not conflicting with inventory.draw
from roll_animation import Animation

import json
# Load item-to-slot mapping from JSON
with open('Game/item_to_slot_count.json', 'r') as file:
    item_to_slot_count = json.load(file)
#save gold from save file
def savegold(var, val):
    with open('Game/gold_save.json', 'r') as file:
        save = json.load(file)

    save[var] = val

    with open('Game/gold_save.json', 'w') as file:
        json.dump(save, file)

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
nfont = pygame.font.SysFont("Comic Sans MS", 20)
gdisplay = mfont.render(f'Gold = {cu.gold}', False, (250, 250, 250))
ldisplay = mfont.render(f'Luck = {round(r.Luck, 1)}', False, (250, 250, 250))
ucost = nfont.render(f'Cost : {100 * (1 + cu.totalupg)}', False, (250, 250, 250))

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
testupgimg = pygame.image.load("Images/upgimg.png").convert_alpha()
equipment_img = pygame.image.load('Images/equipment.png').convert_alpha()
return_img = pygame.image.load("Images/return.png").convert_alpha()
mute_img = pygame.image.load("Images/mute.png").convert_alpha()
open_img = pygame.image.load("Images/opsound.png").convert_alpha()
increase_img = pygame.image.load("Images/icsound.png").convert_alpha()
decrease_img = pygame.image.load("Images/dcsound.png").convert_alpha()
minigame_img = pygame.image.load("Images/minigameicon.png").convert_alpha()


# Create button instances
start_button = Button(300, 450, start_img, width = 450, height = 302)
exit_button = Button(0, 0, exit_img, width = 250, height = 94, effect_enabled = False)
backpack_button = Button(100, 600, backpack_img, width= 100 , height= 95)
roll_button = Button(300, 600, roll_img, width = 249, height = 95)
setting_button = Button(500, 600, setting_img, width = 100, height = 95)
instructions_button = Button(0, 0, instructions_img, width = 250, height = 96)
cross_button = Button(0, 0, cross_img, width = 90, height = 85, effect_enabled = False)
testupg = Button(500, 50, testupgimg, width = 100, height = 50)
equipment_button = Button(100, 450, equipment_img, width=100, height=95)  # Positioned above the inventory button
return_button = Button(0, 0, return_img, width = 75, height = 75, effect_enabled = False)
minigame_button = Button(50, 300, minigame_img, width = 50, height = 50)
mute_button = Button(0, 0, mute_img, width = 72, height = 76)
open_button = Button(0, 0, open_img, width = 75, height = 82)
ic_button = Button(0, 0, increase_img, width = 70, height = 79)
dc_button = Button(0, 0, decrease_img, width = 75, height = 75)

# Define initial volume
volume = 0.5  
pygame.mixer.music.set_volume(volume)

# Define animation paths
common_paths = [f'Images/Sprites/common pic/common_br_{i:03}.png' for i in range(34)]
uncommon_paths = [f'Images/Sprites/uncommon pic/uncommon_br_{i:03}.png' for i in range(34)]
rare_paths = [f'Images/Sprites/rare pic/rare_br_{i:03}.png' for i in range(34)]
epic_paths = [f'Images/Sprites/epic pic/epic_br_{i:03}.png' for i in range(33)]
legendary_paths = [f'Images/Sprites/legendary pic/legendary_br_{i:03}.png' for i in range(33)]
mythic_paths = [f'Images/Sprites/mythic pic/mythic_{i:03}.png' for i in range(33)]
fraud_paths = [f'Images/Sprites/fraud pic/fraud_{i:03}.png' for i in range(32)]
worm_paths = [f'Images/Sprites/worm pic/worm_{i:03}.png' for i in range(33)]
judge_paths = [f'Images/Sprites/judge pic/judge_{i:03}.png' for i in range(33)]
gambler_paths = [f'Images/Sprites/gambler pic/gambler_{i:03}.png' for i in range(32)]
baby_paths = [f'Images/Sprites/baby pic/baby_{i:03}.png' for i in range(33)]
comedian_paths = [f'Images/Sprites/comedian pic/comedian_{i:03}.png' for i in range(33)]
farmer_paths = [f'Images/Sprites/farmer pic/farmer_{i:03}.png' for i in range(32)]
cat_paths = [f'Images/Sprites/cat pic/cat_{i:03}.png' for i in range(32)]
freaky_paths = [f'Images/Sprites/freaky pic/freaky_{i:03}.png' for i in range(32)]
misogynint_paths = [f'Images/Sprites/misogynint pic/misogynint_{i:03}.png' for i in range(32)]
specialz_paths = [f'Images/Sprites/specialz pic/specialz_{i:03}.png' for i in range(32)]
nah_paths = [f'Images/Sprites/nah pic/nah_{i:03}.png' for i in range(32)]
void_paths = [f'Images/Sprites/void pic/void_{i:03}.png' for i in range(33)]
malevolent_paths = [f'Images/Sprites/malevolent pic/malevolent_{i:03}.png' for i in range(33)]

fraud_itempaths = [f'Images/Sprites/fraud item/fraud item_{i:03}.png' for i in range(27)]
worm_itempaths = [f'Images/Sprites/worm item/worm item_{i:03}.png' for i in range(27)]
judge_itempaths = [f'Images/Sprites/judge item/judge item_{i:03}.png' for i in range(27)]
gambler_itempaths = [f'Images/Sprites/gambler item/gambler item_{i:03}.png' for i in range(27)]
baby_itempaths = [f'Images/Sprites/baby item/baby item_{i:03}.png' for i in range(27)]
comedian_itempaths = [f'Images/Sprites/comedian item/comedian item_{i:03}.png' for i in range(27)]
farmer_itempaths = [f'Images/Sprites/farmer item/farmer item_{i:03}.png' for i in range(27)]
cat_itempaths = [f'Images/Sprites/cat item/cat item_{i:03}.png' for i in range(27)]
freaky_itempaths = [f'Images/Sprites/freaky item/freaky item_{i:03}.png' for i in range(27)]
misogynint_itempaths = [f'Images/Sprites/misogynint item/misogynint item_{i:03}.png' for i in range(27)]
specialz_itempaths = [f'Images/Sprites/specialz item/specialz item_{i:03}.png' for i in range(27)]
nah_itempaths = [f'Images/Sprites/nah item/nah item_{i:03}.png' for i in range(27)]
void_itempaths = [f'Images/Sprites/void item/void item_{i:03}.png' for i in range(27)]
malevolent_itempaths = [f'Images/Sprites/malevolent item/malevolent item_{i:03}.png' for i in range(27)]

# Create animation instances
animations = {
    'Common': Animation(common_paths, (450, 253), (75, 95)),
    'Uncommon': Animation(uncommon_paths, (450, 253), (75, 95)),
    'Rare': Animation(rare_paths, (450, 253), (75, 95)),
    'Epic': Animation(epic_paths, (450, 253), (75, 95)),
    'Legendary': Animation(legendary_paths, (450, 253), (75, 95)),
    'Mythic':  Animation(mythic_paths, (450, 253), (75, 95)),
    'Fraud':  Animation(fraud_paths, (450, 253), (75, 95)),
    'Worm':  Animation(worm_paths, (450, 253), (75, 95)),
    'Judge':  Animation(judge_paths, (450, 253), (75, 95)),
    'Gambler':  Animation(gambler_paths, (450, 253), (75, 95)),
    'Baby':  Animation(baby_paths, (450, 253), (75, 95)),
    'Comedian':  Animation(comedian_paths, (450, 253), (75, 95)),
    'Farmer':  Animation(farmer_paths, (450, 253), (75, 95)),
    'Cat':  Animation(cat_paths, (450, 253), (75, 95)),
    'Freaky':  Animation(freaky_paths, (450, 253), (75, 95)),
    'Misogynint':  Animation(misogynint_paths, (450, 253), (75, 95)),
    'Specialz':  Animation(specialz_paths, (450, 253), (75, 95)),
    'Nah':  Animation(nah_paths, (450, 253), (75, 95)),
    'Void':  Animation(void_paths, (450, 253), (75, 95)),
    'Malevolent':  Animation(malevolent_paths, (450, 253), (75, 95)),
}

rarity_item = {
    'Fraud': Animation(fraud_itempaths, (400, 225), (100, 300)),
    'Worm': Animation(worm_itempaths, (400, 225), (100, 300)),
    'Judge': Animation(judge_itempaths, (400, 225), (100, 300)),
    'Gambler': Animation(gambler_itempaths, (400, 225), (100, 300)),
    'Baby':  Animation(baby_itempaths, (400, 225), (100, 300)),
    'Comedian': Animation(comedian_itempaths, (400, 225), (100, 300)),
    'Farmer': Animation(farmer_itempaths, (400, 225), (100, 300)),
    'Cat': Animation(cat_itempaths, (400, 225), (100, 300)),
    'Freaky': Animation(freaky_itempaths, (400, 225), (100, 300)),
    'Misogynint': Animation(misogynint_itempaths, (400, 225), (100, 300)),
    'Specialz': Animation(specialz_itempaths, (400, 225), (100, 300)),
    'Nah': Animation(nah_itempaths, (400, 225), (100, 300)),
    'Void': Animation(void_itempaths, (400, 225), (100, 300)),
    'Malevolent': Animation(malevolent_itempaths, (400, 225), (100, 300)),
}

# Initialize inventory 
inventory = Inventory(screen)

# Panel state
settings_active = False
instruction_active = False
current_animation = None
current_item_animation = None

# Load custom mouse cursor image
cursor_image = pygame.transform.scale(pygame.image.load('Images/cursor.png').convert_alpha(), (40, 39))

def roll():
    global current_animation, current_item_animation

    current_animation = None
    current_item_animation = None
    
    for x in reversed(r.Rarity):
            NotActualFinalChance = (r.FinalChance(1/(r.Rarity[x]), r.Luck, r.Bonus))
            ActualFinalChance = 1/NotActualFinalChance
            try:
                Result = random.randint(1, int(ActualFinalChance))
                if Result == 1:
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
                    if x in animations:
                        current_animation = animations[x]
                        current_animation.reset()

                    if x in rarity_item:
                        current_item_animation = rarity_item[x]
                        current_item_animation.reset()

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

        # Disable other buttons
        for button in [backpack_button, roll_button, setting_button, testupg]:
            button.button_enabled = False

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
            # Enable other buttons
            for button in [backpack_button, roll_button, setting_button, testupg]:
                button.button_enabled = True
        if instructions_button.draw(screen):
            instruction_active = True
        if exit_button.draw(screen):
            #save before quitting
            savegold('gold', cu.gold)
            savegold('totalupgrade', cu.totalupg)
            savegold('passivegain', cu.passivegain)
            savegold('luck', r.Luck)
            inventory.save_item_counts()
            pygame.quit()
            sys.exit()

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
    font = pygame.font.SysFont("Comic Sans MS", 15)
    instruction_text = [
        "Welcome to the MidRNG",
        "1. Roll to get gold and items with increasing rarity.",
        "2. Use gold to make a binding vow at the top ",
        "   right of the screen to earn more gold and luck.",
        "3. Win the minigame to get even more luck.",
        "4. Keep increasing your luck to get the rarest item.",
        "5. To craft in inventory, right click to select and ",
        "   to deselect items."
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

def detect_inventory():
    # If inventory open, disable other buttons
    if inventory.is_open:
        inventory.handle_event(event)
        for button in [roll_button, setting_button, testupg, backpack_button]:
            button.button_enabled = False
    else:
        for button in [roll_button, setting_button, testupg, backpack_button]:
            button.button_enabled = True

def fade_out(width, height):
    fade = pygame.Surface((width, height))
    fade.fill((0, 0, 0))

    for alpha in range(0, 255):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(4)

def update_and_draw_inventory():
    # Check if inventory is open and draw the inventory if it is
    if inventory.is_open:
        inventory.update_animation()  # Call this to update any ongoing animations
        inventory.draw()  # Ensure inventory is drawn when open

# Main loop
running = True
menumouse = True
TempLuck = False
game = mini.minigame1(screen)
clock = pygame.time.Clock()
LastTimeUpdate = pygame.time.get_ticks()
r.Luck += 0.1 * cu.totalupg

while running:
    screen.blit(bg1, (0, 0))
    menumouse = True
    pygame.mouse.set_visible(False)

    if inventory.current_page == 1:
        screen.blit(title, title_rect)
        if start_button.draw(screen):
            fade_out(600, 700)
            inventory.current_page = 2
            
    elif inventory.current_page == 2:
        screen.fill((0, 0, 0))
        gdisplay = mfont.render(f'Gold = {cu.gold}', False, (250, 250, 250))
        ldisplay = mfont.render(f'Luck = {round(r.Luck, 1)}', False, (250, 250, 250))
        ucost = nfont.render(f'Cost : {100 * (1 + cu.totalupg)}', False, (250, 250, 250))
        screen.blit(gdisplay, (10, 0))
        screen.blit(ldisplay, (10, 30))
        screen.blit(ucost, (450, 70))

        # Open inventory button (backpack)
        if backpack_button.draw(screen):
            inventory.open()

        if roll_button.draw(screen):
            roll()

        if setting_button.draw(screen):
            settings_active = True

        if testupg.draw(screen):
            if cu.gold < 100 * (1 + cu.totalupg):
                pass
            else:
                cu.purchase(100 * (1 + cu.totalupg))
                cu.totalupg += 1
                cu.passivegain += 1
                r.Luck += 0.1

        if TempLuck == False:
            if minigame_button.draw(screen):
                menumouse = False
                pygame.mixer.music.pause()
                pygame.mouse.set_visible(False)
                game.run(screen)
                pygame.mixer.music.unpause()

        #Check if pass minigame
        if mini.status == 'Pass':
            r.Luck += 1
            TempLuck = True
            TempLuckTimerOld = pygame.time.get_ticks()
            mini.status = None
        elif mini.status == 'Fail':
            mini.status = None
        
        update_and_draw_inventory()

        # Handle inventory events if it's open
        detect_inventory()
        
        # if minigame_button.draw(screen):
        #     pygame.mouse.set_visible(False)
        #     game.run(screen)
        
        update_and_draw_inventory()  # Redraw the screen after handling logic
            
    # Update and draw the current animation
    if current_animation:
        current_animation.update()
        current_animation.draw(screen)
        if current_animation.finished:
            current_animation = None

        update_and_draw_inventory()

    # Update and draw the current item animation
    if current_item_animation:
        current_item_animation.update()
        current_item_animation.draw(screen)
        if current_item_animation.finished:
            current_item_animation = None 

    if settings_active:
        # Overlay main screen
        overlay = pygame.Surface(screen.get_size())
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150) 
        screen.blit(overlay, (0, 0))
       
        if setting():
            settings_active = False

    #Timer for passive gold gain
    CurrentTime = pygame.time.get_ticks()
    if cu.totalupg > 0 and CurrentTime - LastTimeUpdate >= 1000:
        cu.gold += cu.passivegain
        LastTimeUpdate = CurrentTime

    #Timer for temporary luck after passing minigame
    if TempLuck == True:
        TempLuckTimerNew = pygame.time.get_ticks()
        if TempLuckTimerNew - TempLuckTimerOld >= 5000:
            r.Luck -= 1
            TempLuck = False
            TempLuckTimerNew = TempLuckTimerOld

    # Draw custom mouse cursor
    if menumouse == True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(cursor_image, (mouse_x, mouse_y))

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #save before quitting
            savegold('gold', cu.gold)
            savegold('totalupgrade', cu.totalupg)
            savegold('passivegain', cu.passivegain)
            savegold('luck', r.Luck)
            inventory.save_item_counts()
            running = False   

    pygame.display.update()
    clock.tick(60)

pygame.quit()