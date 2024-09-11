import numpy as np
import pandas as pd
import player_decision_funcs as pdf

# INITIALIZE GAME BOARD ------------------------------------------
def init_game_board():
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
    return P_stats

# GAME FUNCTIONS -------------------------------------------------

def order(P_stats):
    return P_stats.transpose().sample(4, replace=False).index.to_list()

def play_game():
    P_stats = init_game_board()
    print(P_stats)
    rounds = 0
    boss = ''
    play_order = order(P_stats)
    print(f'L\'ordre de jeu est : {play_order}')
    while ((P_stats.transpose()['health'] == 0).sum()) < (len(play_order) - 1) and rounds < 10:
        print(f'joueurs morts : {(P_stats.transpose()['health'] <= 0).sum()}')
        for i in range(4):
            current_player = str(play_order[i])
            if P_stats.loc['health', current_player] > 0:
                print(f'{play_order[i]} a {P_stats.loc['health', current_player]} PV et se prépare à jouer')
                score = pdf.player_plays(P_stats, current_player)
                print(score)
                print(f'{current_player} a un score de {score['score']}')
                if score['score'] == 12 or score['score'] == 30:
                    print(f'{current_player} ne s\'en sort pas trop mal !')
                    continue
                elif score['score'] < 12 or score['score'] > 30:
                    if score['score'] < 12:
                        attack = 12 - score['score']
                        print(f'{current_player} va attaquer au {attack}')
                        damages = pdf.player_attacks(P_stats, current_player, attack)
                        print(f'{current_player} met sa fessée à {damages}')
                        # Degats
                        P_stats.loc['health', damages[0]] = P_stats.loc['health', damages[0]] - damages[1]
                        print(f'{damages[0]} a {P_stats.loc['health', damages[0]]} points de vie restants')
                        print(f'1 - {damages[0]}, 2 - {damages[1]}')
                    else:
                        attack = score['score'] - 30
                        print(f'{current_player} va attaquer au {attack}')
                        damages = pdf.player_attacks(P_stats, current_player, attack)
                        print(f'{current_player} met sa fessée à {damages}')
                        # Degats
                        P_stats.loc['health', damages[0]] = P_stats.loc['health', damages[0]] - damages[1]
                        print(f'{damages[0]} a {P_stats.loc['health', damages[0]]} points de vie restants')
                else:
                    soit = [30 - score['score'], score['score'] - 12]
                    dmg = min(soit)
                    print(f'Ahlala, {current_player} se met {dmg} dégats tout seul {soit}')
                    # Degats
                    P_stats.loc['health', current_player] = P_stats.loc['health', current_player] - dmg
                    print(f'{current_player} a {P_stats.loc['health', current_player]} points de vie restants')
            else:
                print(f'{current_player} est dead mort de chez muerto')

            print(f'Round {rounds}')
        rounds += 1
        boss = str(P_stats.loc['health'].idxmax())
        print(f'{boss} est le boss.')
        print(P_stats)

test = play_game()
print(f'Ordre + selection dernier pl : {test}')

