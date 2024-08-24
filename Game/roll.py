import random
import Rolling as r

def roll():
    for x in r.Rarity:
        NotActualFinalChance = (r.FinalChance(1 / (r.Rarity[x]), r.Luck, r.Bonus))
        ActualFinalChance = 1 / NotActualFinalChance
        Result = random.randint(1, int(ActualFinalChance))
        if Result == 1:
            print(x)
            r.BonusRollCount += 1
            break
