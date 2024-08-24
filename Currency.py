#WIP
import pygame

gold = 100

def gaingold(ammount):
    global gold
    gold += ammount

def purchase(ammount):
    global gold
    gold -= ammount

#tinput = rollgold(int(input()))