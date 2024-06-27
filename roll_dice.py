import numpy as np
import pandas as pd

# PLAYERS, GAME, STATS ------------------------------------------
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

# ROLL THE DICES -------------------------------------------------
def RollD():
    result = np.random.randint(1,7)
    return result

starting_dices = 6
def Hand_Roll(starting_dices):
    res = []
    for d in range(starting_dices):
        d = RollD()
        res.append(d)
    return res

# DECISION FILTERS -----------------------------------------------
def main_filter(hi_dot_bet, chosen, list, player):
    suggestion = []
    if P_stats.loc['cautious', player]:
        if hi_dot_bet:
            for i in list:
                if i == 6:
                    suggestion.append(i)
            if len(suggestion) > 0:
                for i in suggestion:
                    list.remove(i)
                if np.sum(chosen) + np.sum(suggestion) + np.sum(list) > 30 and np.median(list) > 4:
                    if P_stats.loc['consistent', player]*0.8 >= np.random.rand()*10:
                        for i in list:
                            suggestion.append(i)
                        return suggestion
                return suggestion
            else:
                maxi = max(list)
                suggestion.append(maxi)
                return suggestion
        else:
            for i in list:
                if i == 1:
                    suggestion.append(i)
            if len(suggestion) > 0:
                for i in suggestion:
                    list.remove(i)
                if np.sum(chosen) + np.sum(suggestion) + np.sum(list) < 12 and np.median(list) < 3:
                    if P_stats.loc['consistent', player]*0.8 >= np.random.rand()*10:
                        for i in list:
                            suggestion.append(i)
                        return suggestion
                return suggestion
            else:
                mini = min(list)
                suggestion.append(mini)
                return suggestion
    # NON CAUTIOUS PLAYER
    else:
        if hi_dot_bet:
            for i in list:
                if i == 6:
                    suggestion.append(i)
            if len(suggestion) > 0:
                for i in suggestion:
                    list.remove(i)
                for i in list:
                    if ((np.sum(chosen) + i)/(len(chosen)+1)) > 5.5:
                        if P_stats.loc['consistent', player] >= np.random.rand()*10:
                            suggestion.append(i)
                return suggestion
            else:
                if len(chosen) == 1 and list.count(1) >= 2:
                    if P_stats.loc['consistent', player] >= np.random.rand()*10:
                        for i in list:
                            if i == 1:
                                suggestion.append(i)
                            elif i == 2:
                                if P_stats.loc['consistent', player]*0.3 >= np.random.rand()*10:
                                    suggestion.append(i) 
                if len(suggestion) > 0:
                    return suggestion
                else:
                    maxi = max(list)
                    suggestion.append(maxi)
                    return suggestion
        else:
            for i in list:
                if i == 1:
                    suggestion.append(i)
            if len(suggestion) > 0:
                for i in suggestion:
                    list.remove(i)
                for i in list:
                    if ((np.sum(chosen) + i)/(len(chosen)+1)) < 1.5:
                        if P_stats.loc['consistent', player] >= np.random.rand()*10:
                            suggestion.append(i)
                return suggestion
            else:
                if len(chosen) == 1 and list.count(6) >= 2:
                    if P_stats.loc['consistent', player] >= np.random.rand()*10:
                        for i in list:
                            if i == 6:
                                suggestion.append(i)
                            elif i == 5:
                                if P_stats.loc['consistent', player]*0.3 >= np.random.rand()*10:
                                    suggestion.append(i)
                if len(suggestion) > 0:
                    return suggestion
                else:
                    mini = min(list)
                    suggestion.append(mini)
                    return suggestion

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
    

def filter_lo(list):
    count_twos = list.count(2)
    count_fives = list.count(5)

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
# END DECISION FILTERS -------------------------------------------

# PLAYING FUNCTIONS ----------------------------------------------
def set_bet(choix_tac):
    if np.mean(choix_tac) < 3.5:
        return False
    elif np.mean(choix_tac) > 3.5:
        return True

def player_plays(player):
    hidot_bet = True
    acrobatie = False
    if np.random.rand() < 0.5:
        hidot_bet = False
    choix = []

    # 1st RUN -----------------------
    res = Hand_Roll(starting_dices)
    decision = filter_hi(res, player)

    if decision == ['X']:
        decision = filter_lo(res)
        if decision == ['X']:
            if hidot_bet == False:
                if 3 in res:
                    choix.append(3)
                else:
                    choix.append(4)
            elif hidot_bet == True:
                if 4 in res:
                    choix.append(4)
                else:
                    choix.append(3)
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

    hidot_bet = set_bet(choix)
    test_acrobatie = set_bet(choix)
    
    if len(choix) == 6:
        return {
            'run' : 1,
            'score' : int(np.sum(choix)),
            'decision' : choix,
            'acrobatie' : acrobatie
            }
    else:
        # 2ND RUN -----------------------------------
        res = Hand_Roll(starting_dices - len(choix))
        decision = main_filter(hidot_bet, choix, res, player)
        for d in decision:
            choix.append(d)

        hidot_bet = set_bet(choix)
        if hidot_bet != test_acrobatie:
            acrobatie = True

        if len(choix) == 6:
            print(f'{player} se met très bien dès le deuxième tour !')
            return {
                'run' : 2,
                'score' : int(np.sum(choix)),
                'decision' : choix,
                'acrobatie' : acrobatie
                }
        else:
            #3RD RUN -----------------------------------
            res = Hand_Roll(starting_dices - len(choix))
            decision = main_filter(hidot_bet, choix, res, player)
            for d in decision:
                choix.append(d)

            if len(choix) == 6:
                return {
                    'run' : 3,
                    'score' : int(np.sum(choix)),
                    'decision' : choix,
                    'acrobatie' : acrobatie
                    }
            else:
                #4TH RUN -----------------------------------
                res = Hand_Roll(starting_dices - len(choix))
                decision = main_filter(hidot_bet, choix, res, player)
                for d in decision:
                    choix.append(d)

                if len(choix) == 6:
                    return {
                        'run' : 4,
                        'score' : int(np.sum(choix)),
                        'decision' : choix,
                        'acrobatie' : acrobatie
                        }
                else:
                    #5TH RUN -----------------------------------
                    res = Hand_Roll(starting_dices - len(choix))
                    decision = main_filter(hidot_bet, choix, res, player)
                    for d in decision:
                        choix.append(d)

                    if len(choix) == 6:
                        return {
                            'run' : 5,
                            'score' : int(np.sum(choix)),
                            'decision' : choix,
                            'acrobatie' : acrobatie
                            }
                    else:
                        #LAST RUN ----------------------------------
                        res = Hand_Roll(starting_dices - len(choix))
                        decision = main_filter(hidot_bet, choix, res, player)
                        for d in decision:
                            choix.append(d)

                        if len(choix) == 6:
                            return {
                                'run' : 6,
                                'score' : int(np.sum(choix)),
                                'decision' : choix,
                                'acrobatie' : acrobatie
                                }
                        else:
                            print(f'Error')
# END PLAYING FUNCTIONS ----------------------------------------------

player = 'Pavard'
score = player_plays(player)
print(f'{player} nous régale : {score}')