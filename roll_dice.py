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

# DECISION FILTERS
def filter_uncautious_greed(chosen, list, player):
    shrink_list = []
    suggestion = []
    for i in list:
        if i not in [1, 6]:
            shrink_list.append(i)
    for i in shrink_list:
        if ((np.sum(chosen) + i)/(len(chosen)+1)) > 5:
            suggestion.append(i)
        elif ((np.sum(chosen) + i)/(len(chosen)+1)) < 2:
            suggestion.append(i)

    possible_avg = (np.sum([np.sum(chosen) , np.sum(suggestion)]))/(len(chosen) + len(suggestion))

    if P_stats.loc['consistent', player]*1.5 >= np.random.rand()*10:
        if len(chosen) + len(suggestion) == 6 and possible_avg > 5:
            return suggestion
        elif len(chosen) + len(suggestion) == 6 and possible_avg < 2:
            return suggestion
        
    if 2 in suggestion or 3 in suggestion:
        suggestion.sort(reverse=True)
    else:
        suggestion.sort()

    if possible_avg < 5.31 and possible_avg > 5:
        del(suggestion[0])
    elif possible_avg > 1.59 and possible_avg < 2:
        del(suggestion[0])

    if 3 in suggestion and 2 not in suggestion:
        return ['X']
    if 4 in suggestion and 5 not in suggestion:
        return ['X']

    if P_stats.loc['consistent', player] >= np.random.rand()*10 and len(suggestion) > 0:
        return suggestion
    else:
        return ['X']
    

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
            return filtered_hi_up, filtered_hi_down



# PLAYER PLAYS

player = 'Ronaldinho'
def player_plays(player):
    hidot_bet = True
    if np.random.rand() < 0.5:
        hidot_bet = False
    choix = []
    res = Hand_Roll(starting_dices)
    #res = [3,1,1,1,2,3]
    decision = filter_hi(res, player)
    
    if decision == ['X']:
        decision = filter_lo_no_up(res, player)
        if decision == ['X']:
            if hidot_bet == False:
                choix.append(3)
            if hidot_bet == True:
                choix.append(4)
        else:
            if P_stats.loc['cautious', player]:
                if hidot_bet:
                    if 5 in decision:
                        choix.append(5)
                    else:
                        choix.append(2)
                else:
                    if 2 in decision:
                        choix.append(2)
                    else:
                        choix.append(5)

            #Joueur cautious = false pour du 5|2
            else:
                if len(decision) == 2 and type(decision[0]) == list:
                    if P_stats.loc['consistent', player]*2 >= np.random.rand()*10:
                        if hidot_bet:
                            if 5 in decision:
                                choix.append(5)
                            else:
                                choix.append(2)
                        else:
                            if 2 in decision:
                                choix.append(2)
                            else:
                                choix.append(5)
                    else:
                        if len(decision[0]) > len(decision[1]):
                            for i in decision[0]:
                                choix.append(i)
                        else:
                            for i in decision[1]:
                                choix.append(i)
                else:
                    if P_stats.loc['consistent', player]*2 >= np.random.rand()*10:
                        choix.append(decision[0])
                    else:
                        for i in decision:
                            choix.append(i)
    # Joueurs pour le 6|1
    else:
        if P_stats.loc['cautious', player]:
            if len(decision) == 2 and type(decision[0]) == list:
                for i in decision[0]:
                    choix.append(i)
            else:
                for i in decision:
                    choix.append(i)
            print(f'{player} est prudent. Il a choisi {choix} au premier jet.')
        else:
            if len(decision) == 2 and type(decision[0]) == list:
                if P_stats.loc['consistent', player]*2 >= np.random.rand()*10:
                    for i in decision[0]:
                        choix.append(i)
                else:
                    for i in decision[1]:
                        choix.append(i)
            else:
                for i in decision:
                    choix.append(i)

            greed = filter_uncautious_greed(choix, res, player)
            if greed == ['X']:
                pass
            else:
                for i in greed:
                    choix.append(i)

        
    # END OF 1ST RUN
    print(f'{player} a choisi : {choix}')
    print(f'nombre de dés choisis : {len(choix)}')
    if np.mean(choix) < 3:
        hidot_bet = False
    if np.mean(choix) > 4:
        hidot_bet = True
        
    if len(choix) == 6:
        return choix
    if len(choix) != 6:
        print('le tour n\'est pas terminé !!!')
    
    # 2ND RUN
    print(f'{player} est en train de parier haut: {hidot_bet}')

    for d in res:
        print(d)

player_plays(player)