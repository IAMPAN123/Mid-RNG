#WIP
import pygame

gold = 0

def rollgold(ammount):
    global gold
    gold += ammount

tinput = rollgold(int(input()))