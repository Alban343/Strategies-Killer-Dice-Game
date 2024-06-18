import numpy as np
import pandas as pd

# PLAYERS
players = ['Bobby', 'Pavard', 'Ronaldinho']
P_stats_d = {}
for p in players:
    stat = open(str(f'P_{p}.txt'), 'r')
    line = []
    for l in stat:
        line.append(l.replace('\n',''))
    P_stats_d[line[0]] = [line[1].split(',')[1],line[2].split(',')[1],line[3].split(',')[1]]
    stat.close()

P_stats = pd.DataFrame(P_stats_d)
print(P_stats)

# ROLL THE DICES
def RollD():
    result = np.random.randint(1,7)
    return result

Starting_dices = 6

def Init_Roll(starting_dices):
    score = []
    for d in range(starting_dices):
        d = RollD()
        score.append(d)
    print(score)

