import csv
from datetime import date


def get_max_score():
    rows = []
    with open('scores.csv', 'a+') as f:
        f.seek(0)
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            try:
                rows.append(int(row[0]))
            except:
                continue
    if len(rows) > 0:
        max_score = sorted(rows, reverse=True)
        return max_score[0]


def save_score(score, timer, speed_level, max_combo):
    with open('scores.csv', 'a+') as f:
        f.seek(0)
        data = f.read(100)
        if len(data) == 0:
            f.write('No.,Score,Time,Speed Level,Max Combo, Date\n')

        else:
            f.write('\n')
        f.write(f'{str(score)},{timer},{speed_level},{max_combo},{date.today()}')


def get_score_factor(speed_level, combo):
    score_factor = speed_level + combo * 10
    return score_factor
