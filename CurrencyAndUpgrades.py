#WIP
import pygame

gold = 100

#Gold
if gold < 0:
    gold = 0

def gaingold(amount):
    global gold
    gold += amount

def purchase(amount):
    global gold
    if amount > gold:
        pass
    else:
        gold -= amount

#Upgrade
totalupg = 0
passivegain = 0

#tinput = rollgold(int(input()))