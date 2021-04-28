import csv
from datetime import date


class Player(object):
    def __init__(self):
        self.speed = 1
        self.extra_speed = 0
        self.score = 0
        self.timer = 0
        self.speed_level = 30
        self.start_speed_level = 30
        self.fall_speed = 0.45 - self.start_speed_level * 0.005
        self.start_fall_speed = 0.45 - self.start_speed_level * 0.005
        self.combo = 0
        self.max_combo = 0
        self.name = ''

    @staticmethod
    def get_max_score():
        rows = []
        with open('scores.csv', 'a+') as f:
            f.seek(0)
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                rows.append(int(row[1]))
        if len(rows) > 0:
            max_score = sorted(rows, reverse=True)
            return max_score[0]

    def format_timer(self):
        mins = self.timer // 60
        formatted_mins = f'0{mins}' if mins < 10 else mins
        secs = self.timer - mins * 60
        formatted_secs = f'0{secs}' if secs < 10 else secs
        formatted_timer = f'{formatted_mins}:{formatted_secs}'

        return formatted_timer

    def save_score(self, formatted_timer):
        with open('scores.csv', 'a+') as f:
            f.seek(0)
            data = f.read(100)
            if len(data) > 0:
                f.write('\n')
            f.write(f'{self.name},{str(self.score)},{self.speed_level},{formatted_timer()},{self.max_combo},{date.today()}')

    def get_score_factor(self):
        score_factor = self.speed_level + self.combo * 10
        return score_factor

    def restart_stats(self):
        self.timer = 0
        self.max_combo = 0
        self.speed_level = self.start_speed_level
        self.fall_speed = self.start_fall_speed
        self.name = ''
