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

def filter_lo_no_up(list, player):
    count_twos = list.count(2)
    count_fives = list.count(5)
    print(count_twos, count_fives)
    if count_twos == 0 and count_fives == 0:
        return ['X']
    
    if count_twos > count_fives:
        most_frequent = 2
        less_frequent = 5
    elif count_fives > count_twos:
        most_frequent = 5
        less_frequent = 2
    else:
        if np.random.rand() < 0.5:
            most_frequent = 2
            less_frequent = 5
        else:
            most_frequent = 5
            less_frequent = 2

    filtered_lo_up = []
    for num in list:
        if num == most_frequent:
            filtered_lo_up.append(num)
    filtered_lo_down = []
    for num in list:
        if num == less_frequent:
            filtered_lo_down.append(num)

    if filtered_lo_down == []:
        return filtered_lo_up
    else:
        return filtered_lo_up, filtered_lo_down


def filter_hi(list, player):
    count_ones = list.count(1)
    count_sixes = list.count(6)

    if count_ones == 0 and count_sixes == 0:
        return ['X']
    
    if count_ones > count_sixes:
        most_frequent = 1
        less_frequent = 6
    elif count_sixes > count_ones:
        most_frequent = 6
        less_frequent = 1
    else:
        if np.random.rand() < 0.5:
            most_frequent = 1
            less_frequent = 6
        else:
            most_frequent = 6
            less_frequent = 1

    filtered_hi_up = []
    for num in list:
        if num == most_frequent:
            filtered_hi_up.append(num)
    filtered_hi_down = []
    for num in list:
        if num == less_frequent:
            filtered_hi_down.append(num)

    if P_stats.loc['cautious', player]:
        return filtered_hi_up
    else:
        if filtered_hi_down == []:
            return filtered_hi_up
        else:
            if P_stats.loc['consistent', player] >= np.random.rand()*10:
                return filtered_hi_up
            else:
                return filtered_hi_down



# PLAYER PLAYS

player = 'Ronaldinho'
def player_plays(player):
    hidot_bet = True
    if np.random.rand() < 0.5:
        hidot_bet = False
    choix = []
    res = Hand_Roll(starting_dices)
    decision = filter_hi(res, player)
    
    if decision == ['X']:
        decision = filter_lo_no_up(res, player)
        if decision == ['X']:
            if hidot_bet == False:
                choix.append(3)
            if hidot_bet == True:
                choix.append(4)
        else:
            print(f'le joueur va devoir se contenter de pas grand chose : {decision}')
            #Coder la fonction pour choisir 5 ou 2
    else:
        for d in decision:
            choix.append(d)
        #Coder ici une propriété de consistent pour quelqu'un qui voudrait ajouter un dé assez fort
        
        # 2ND RUN
        print(f'le joueur a choisi : {choix}')
        if np.mean(choix) < 3:
            hidot_bet = False
        if np.mean(choix) > 4:
            hidot_bet = True
    print(hidot_bet)

    for d in res:
        print(d)

player_plays(player)