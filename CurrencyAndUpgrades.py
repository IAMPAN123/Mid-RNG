#WIP
import pygame

gold = 100
UpgUnlocked = False

#Gold
if gold < 0:
    gold = 0

def gaingold(ammount):
    global gold
    gold += ammount

def purchase(ammount):
    global gold
    gold -= ammount

#Upgrade
totalupg = 0
testupg = 0
passivegain = 0

if totalupg >= 1:
    UpgUnlocked = True

#tinput = rollgold(int(input()))