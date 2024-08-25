#WIP
import pygame

gold = 100

if gold < 0:
    gold = 0

def gaingold(ammount):
    global gold
    gold += ammount

def purchase(ammount):
    global gold
    gold -= ammount

#tinput = rollgold(int(input()))