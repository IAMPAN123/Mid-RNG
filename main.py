import pygame
from button import Button
from Game.inventory import Inventory
from Game.roll import roll
from Game.gui import draw_inventory

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((600, 700))
pygame.display.set_caption("Roll")

# Load button images
start_img = pygame.image.load("Images/start.png").convert_alpha()
exit_img = pygame.image.load("Images/exit.png").convert_alpha()
menu_img = pygame.image.load("Images/menu.png").convert_alpha()
roll_img = pygame.image.load("Images/roll.png").convert_alpha()
setting_img = pygame.image.load("Images/setting.png").convert_alpha()

# Create button instances
start_button = Button(160, 250, start_img, width=300, height=150)
exit_button = Button(20, 30, exit_img, width=50, height=50)
backpack_button = Button(50, 500, menu_img, width=150, height=78)
roll_button = Button(222, 496, roll_img, width=150, height=88)
setting_button = Button(400, 504, setting_img, width=150, height=78)

# Initialize inventory
inventory = Inventory(screen)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((202, 228, 241))

    if inventory.current_page == 1:
        if start_button.draw(screen):
            print("Start")
            inventory.current_page = 2
        if exit_button.draw(screen):
            running = False
    elif inventory.current_page == 2:
        screen.fill((204, 135, 230))

        if backpack_button.draw(screen):
            inventory.open()
        if roll_button.draw(screen):
            roll()
        if setting_button.draw(screen):
            print("Settings open")
        if inventory.is_open:
            draw_inventory(screen, inventory)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        inventory.handle_event(event)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
