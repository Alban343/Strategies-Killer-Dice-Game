import numpy as np

# ROLL THE DICES
def RollD():
    result = np.random.randint(1,7)
    return result

def Init_Roll(starting_dices):
    score = []
    for d in range(starting_dices):
        d = RollD()
        score.append(d)
    print(score)

Init_Roll(6)