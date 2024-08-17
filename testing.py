import pygame

pygame.init()

#set up screen
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Roll")

#set up colour 

#set up background
background_image1 = pygame.image.load("bg1.jpg")
background_image2 = pygame.image.load("bg1.jpg")
start_button = pygame.image.load("start.png")

background_size = (800,600)
button_size = (100,50)

resized_image1 = pygame.transform.scale(background_image1, (background_size))
resized_image = pygame.transform.scale(start_button, (button_size))


#set up font

#button
class Button:
    #load img
    def __init__(self, image_path, x, y, action=None):
        self.image =pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.action = action

    #draw img
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    #handle user input
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

#page
page = "start"

#change to next page
def start():
    global page
    page = "load in" 

def backpack():
    print("背包按钮被点击！")

def roll():
    print("骰子按钮被点击！")

def menu():
    print("主页按钮被点击！")

# button display
start_button = Button("start.png", 300, 250, start)
menu_button = Button("start.png", 100, 500, backpack)
roll_button = Button("start.png", 325, 500, roll)
home_button = Button("start.png", 550, 500, menu)

#main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if page == "start":
            start_button.handle_event(event)
        elif page == "second":
            menu_button.handle_event(event)
            roll_button.handle_event(event)
            home_button.handle_event(event)

        if page == "start":
            screen.blit(resized_image1,(0,0))
            start_button.draw(screen)
            screen.blit(resized_image,(0,0))
        elif page == "second":
            screen.blit(background_image2,(0,0))
            menu_button.draw(screen)
            roll_button.draw(screen)
            home_button.draw(screen)
    
    pygame.display.flip()

pygame.quit()