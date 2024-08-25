import pygame
import button as b
import Currency as c
import time as t

#Upgrde button images
testupgimg = pygame.image.load('Images/placeholder.png').convert_alpha()

#Upgrade buttons
testupg = b.Button(0, 0, testupgimg, width = 100, height = 50)

#Upgrade functions
def UpgPassiveIncome(amount):
    while True:
        c.gaingold(amount)
        t.sleep(1)