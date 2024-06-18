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
    P_stats_d[line[0]] = [30, bool(int(line[1].split(',')[1])), int(line[2].split(',')[1]), int(line[3].split(',')[1])]
    stat.close()
col_names = ['health', 'cautious','consistent','attack']
P_stats = pd.DataFrame(P_stats_d, index=col_names)
print(P_stats)

# ROLL THE DICES
def RollD():
    result = np.random.randint(1,7)
    return result

starting_dices = 6
def Hand_Roll(starting_dices):
    score = []
    for d in range(starting_dices):
        d = RollD()
        score.append(d)
    return score

# DECISIONS FILTER

def filter_hi(list):
    count_ones = list.count(1)
    count_sixes = list.count(6)
    
    if count_ones > count_sixes:
        most_frequent = 1
        less_frequent = 6
    elif count_sixes > count_ones:
        most_frequent = 6
        less_frequent = 1
    else:
        if np.random.rand() < 0.5:
            most_frequent = 1
        else:
            most_frequent = 6

    filtered_up = [num for num in list if num == most_frequent]
    filtered_down = [num for num in list if num == less_frequent]

    return filtered_up, filtered_down



# PLAYER PLAYS
player = 'Pavard'
def player_plays(player):
    choix = []
    res = Hand_Roll(starting_dices)
    decision = filter_hi(res)
    print(decision)

    for d in res:
        print(d)
        choix.append(d)

player_plays(player)