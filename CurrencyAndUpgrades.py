#WIP
import pygame
import Game.inventory as gi
import json as js

def loadgold():
    try:
        with open('Game/gold_save.json', 'r') as file:
            return js.load(file)
    except FileNotFoundError:
        # Handle file not found error
        return {}

load = loadgold()

gold = load["gold"]

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
totalupg = load["totalupgrade"]
passivegain = load["passivegain"]

#tinput = rollgold(int(input()))