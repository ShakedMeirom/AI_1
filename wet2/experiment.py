from subprocess import call
import threading
import re
from matplotlib import pyplot as plt
import os
import shutil

players = ['simple_player', 'better_player', 'alpha_beta_player', 'min_max_player']
times = ['2', '10', '50']
PYTHON = r'C:\Users\Shaked\AppData\Local\Programs\Python\Python35\python.exe'
def callto(p1):

    for p2 in players:
        for time in times:
            if p1 == p2:
                continue

            file_name = 'temp/' + p1 + p2+time+'.txt'
            file = open(file_name, 'w+')

            for _ in range(5):
                print(PYTHON + ' run_game.py 2 {} 5 n {} {}'.format(time, p1, p2))
                call([PYTHON, 'run_game.py', '2', time, '5', 'n', p1, p2], stdout=file)

            file.close()


def run_threads():
    threads = []

    for p1 in ['simple_player', 'better_player']:
        t = threading.Thread(target=callto, args=[p1])
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    for p1 in ['alpha_beta_player', 'min_max_player']:
            t = threading.Thread(target=callto, args=[p1])
            threads.append(t)
            t.start()

    for t in threads:
            t.join()


def create_fianl_reult_and_csv_file():
    final_result = {player: {t: 0 for t in times} for player in players}
    final = open('final.csv', 'w')
    for p1 in players:
        for p2 in players:
            if p1 == p2:
                continue
            for time in times:
                file_name = 'temp/' + p1 + p2+time+'.txt'
                with open(file_name, 'r') as file:
                    for line in file.readlines():
                        if "winner" in line:
                            winner = re.split('\n', line)[0].split(' ')[-1] + '_player'
                            p1_score = '0.5'
                            p2_score = '0.5'
                            if winner == p1:
                                p1_score = '1'
                                p2_score = '0'
                            elif winner == p2:
                                p1_score = '0'
                                p2_score = '1'
                            final_result[p1][time] += float(p1_score)
                            final_result[p2][time] += float(p2_score)
                            line_to_print = p1 + ',' + p2 + ',' + time + ',' + p1_score + ',' + p2_score + '\n'
                            final.write(line_to_print)
                        else:
                            print('line is:{}'.format(line))
    final.close()
    return final_result


def create_graph_and_final_table(final_result):
    final_table = open('experiments.csv', 'w')
    headers = 't = 2, t = 10, t = 50, player_name\n'
    final_table.write(headers)
    plt.figure()
    x = [float(t) for t in times]
    plt.title('Score as a function of t')
    for player in players:
        time_to_point = final_result[player]
        y = [time_to_point[t] for t in times]
        line = ''
        for point in y:
            line += str(point) + ','
        line += player + '\n'
        final_table.write(line)
        plt.plot(x, y, '.-', label=player)
    final_table.close()
    plt.legend()
    plt.show()


def main():

    if not os.path.isdir('temp'):
        os.mkdir('temp')

    run_threads()
    final_result = create_fianl_reult_and_csv_file()
    create_graph_and_final_table(final_result)

    #if os.path.isdir('temp'):
    #    shutil.rmtree('temp')


if __name__ == '__main__':
    main()
