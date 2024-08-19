import random
#Rolling and Luck
#Luck variables
Base = 1
Bonus = 1
BonusRollCount = 0
#Luck Calulation
Luck = Base
if BonusRollCount == 10:
    Bonus = 2
elif BonusRollCount > 10:
    Bonus = 1
    BonusRollCount = 0
#if Equipment == True:
#    Bonus *= Multiplier
#else:
#    Bonus = 1
#Item rarity
Rarity = {'Legendary' : 10, 'Epic' : 8, 'Rare' : 4, 'Uncommon' : 2, 'Common' : 1}
#Rolling Calulation
def FinalChance(Chance, Luck, Bonus):
    RollChance = Chance*((Luck*Bonus))
    return(RollChance)
#Rolling System
#run = True
#while run:
#    userinput = input()
#    if userinput == 'roll':
#        for x in Rarity:
#            NotActualFinalChance = (FinalChance(1/(Rarity[x]), Luck, Bonus))
#            ActualFinalChance = 1/NotActualFinalChance
#            Result = random.randint(1, int(ActualFinalChance))
#            if Result == 1:
#                print(x)
#                BonusRollCount += 1
#                break
#            else:
#                continue
#    elif userinput == 'exit':
#        run = False
#    else:
#        print('Input error')