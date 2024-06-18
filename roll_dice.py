import numpy as np
import pandas as pd

# PLAYERS
players = ['Bobby', 'Pavard', 'Ronaldinho', 'Mec_Raide']
P_stats_d = {}
for p in players:
    stat = open(str(f'P_{p}.txt'), 'r')
    line = []
    for l in stat:
        line.append(l.replace('\n',''))
    P_stats_d[line[0]] = [30, int(line[1].split(',')[1]), int(line[2].split(',')[1]), int(line[3].split(',')[1])]
    stat.close()
col_names = ['health', 'cautious','consistent','attack']
P_stats = pd.DataFrame(P_stats_d, index=col_names)

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
    return score


print(Init_Roll(Starting_dices))
