import random
#Rolling and Luck
#Luck variables
Base = 1
UpgradeLuck = 0
EquipmentLuck = 0
MinigameLuck = 0
PotionLuck = 0
Bonus = 1
BonusRollCount = 0
#Luck Calulation
Luck = Base + UpgradeLuck + EquipmentLuck + MinigameLuck + PotionLuck
#print(Luck)
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
TestList = []
run = True
while run:
    userinput = input()
    if userinput == 'roll':
        rolls = 1000
        while rolls > 0:
            for x in Rarity:
                NotActualFinalChance = (FinalChance(1/(Rarity[x]), Luck, Bonus))
                ActualFinalChance = 1/NotActualFinalChance
                print(f'{x} = {int(ActualFinalChance)}')
                try:
                    Result = random.randint(1, int(ActualFinalChance))
                    if Result == 1:
                        rollresult = x
                        TestList.append(str(rollresult))
                        BonusRollCount += 1
                        if BonusRollCount == 10:
                            Bonus = 2
                        elif BonusRollCount > 10:
                            Bonus = 1
                            BonusRollCount = 0
                        #print(BonusRollCount, Bonus)
                        rolls -= 1
                    else:
                        continue
                except ValueError:
                    print('ValueError')
        #print(TestList)
        legen = TestList.count('Legendary')
        ep = TestList.count('Epic')
        ra = TestList.count('Rare')
        unc = TestList.count('Uncommon')
        com = TestList.count('Common')
        print(f'Legendary = {legen}\n',f'Epic = {ep}\n',f'Rare = {ra}\n',f'Uncommon = {unc}\n',f'Common = {com}\n')
        TestList.clear()
    elif userinput == 'exit':
        run = False
    else:
        print('Input error')
