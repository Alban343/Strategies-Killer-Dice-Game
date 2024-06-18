import numpy as np

# ROLL THE DICES
def RollD():
    result = np.random.randint(1,7)
    return result

def Init_Roll():

score1 = RollD()
print(score1)
