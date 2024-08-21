import pygame
import button
import random
import Rolling as r
import Currency as c

pygame.init()
pygame.font.init()

#set up screen
screen = pygame.display.set_mode((600,700))
pygame.display.set_caption("Roll")

#set up text and font
mfont = pygame.font.SysFont("Comic Sans MS", 30)
gdisplay = mfont.render(f'Gold = {c.gold}', False, (0, 0, 0))

#set up bg
#background_image1 = pygame.image.load("")
#background_image2 = pygame.image.load("")

#set up button
start_img = pygame.image.load("Images/start.png").convert_alpha()
exit_img = pygame.image.load("Images/exit.png").convert_alpha()
menu_img = pygame.image.load("Images/menu.png").convert_alpha()
roll_img = pygame.image.load("Images/roll.png").convert_alpha()
setting_img = pygame.image.load("Images/setting.png").convert_alpha()

#create button instances
start_button = button.Button(160, 250, start_img, width = 300, height = 150)
exit_button = button.Button(20, 30, exit_img, width = 50, height = 50)
backpack_button = button.Button(50, 500, menu_img, width = 150, height = 78)
roll_button = button.Button(222, 496, roll_img, width = 150, height = 88)
setting_button = button.Button(400, 504, setting_img, width = 150, height = 78)

#define function
def menu():
    print("beg open")

def roll():
    for x in r.Rarity:
            NotActualFinalChance = (r.FinalChance(1/(r.Rarity[x]), r.Luck, r.Bonus))
            ActualFinalChance = 1/NotActualFinalChance
            try:
                Result = random.randint(1, int(ActualFinalChance))
                if Result == 1:
                    print(x)
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
    print("setting open")

#page
current_page = 1

#main loop
running = True
while running:
    
    screen.fill((202, 228, 241))

    if current_page == 1:

        if start_button.draw(screen):
            print("Start")
            current_page = 2
        if exit_button.draw(screen):
            running = False

    elif current_page == 2:
        screen.fill((204,135,230))
        screen.blit(gdisplay, (10, 0))

        if backpack_button.draw(screen):
            menu()
        if roll_button.draw(screen):
            roll()
        if setting_button.draw(screen):
            setting()

    #event handler
    for event in pygame.event.get():
		#quit game
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()

pygame.quit()