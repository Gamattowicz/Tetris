import pygame
import random
import sys
import csv

# SIZE OF SCREEN
WIDTH, HEIGHT = 800, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TETRIS')
pygame.init()

# SIZE OF BOX
BLOCK_SIZE: int = 30
BOX_WIDTH, BOX_HEIGHT = 10 * BLOCK_SIZE, 20 * BLOCK_SIZE

# BEGIN POINT OF BOX
START_BOX_X = (WIDTH - BOX_WIDTH) // 2
START_BOX_Y = HEIGHT - BOX_HEIGHT

# FONTS
TITLE_FONT = pygame.font.SysFont('arial', 60)
PREVIEW_FONT = pygame.font.SysFont('arial', 20)
SCORE_FONT = pygame.font.SysFont('arial', 25)
LOST_FONT = pygame.font.SysFont('arial', 95)

# SHAPE FORMATS
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

SHAPES = [S, Z, I, O, J, L, T]
SHAPE_COLORS = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0),
                (255, 165, 0), (0, 0, 255), (128, 0, 128)]
active = 1
speed = 1
mode = 1
extra_speed = 0
timer = 0


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0


def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for i in range(10)] for i in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


def draw_grid(surface, grid):
    sx = START_BOX_X
    sy = START_BOX_Y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (START_BOX_X, START_BOX_Y + i * BLOCK_SIZE),
                         (START_BOX_X + BOX_WIDTH,
                          START_BOX_Y + i * BLOCK_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (START_BOX_X + j * BLOCK_SIZE, START_BOX_Y),
                             (START_BOX_X + j * BLOCK_SIZE,
                              START_BOX_Y + BOX_HEIGHT))


def get_shape():
    return Piece(5, 0, random.choice(SHAPES))


def convert_shape_format(block):
    positions = []
    variety = block.shape[block.rotation % len(block.shape)]

    for i, row in enumerate(variety):
        for j, column in enumerate(row):
            if '0' in column:
                positions.append((block.x + j, block.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    free_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    free_pos = [j for sub in free_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in free_pos:
            if pos[1] > -1:
                return False
    return True


def draw_window(surface, grid):
    surface.fill((0, 0, 0))

    # draw title over the box
    title = TITLE_FONT.render('TETRIS', 1, (255, 255, 255))
    surface.blit(title, (START_BOX_X + BOX_WIDTH / 2 - (title.get_width() / 2), 20))

    # draw each brick
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (START_BOX_X + j * BLOCK_SIZE, START_BOX_Y + i * BLOCK_SIZE,
                                                   BLOCK_SIZE, BLOCK_SIZE), 0)

    # draw border of box
    pygame.draw.rect(surface, (255, 0, 0), (START_BOX_X, START_BOX_Y, BOX_WIDTH, BOX_HEIGHT), 5)

    draw_grid(surface, grid)


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def draw_lost_text(WIN):
    global active
    lost = True

    while lost:
        WIN.fill((0, 0, 0))
        lost_text = LOST_FONT.render('YOU LOST!', 1, (255, 255, 255))
        WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 3))

        retry_text = TITLE_FONT.render('Do you want to play again?', 1, (255, 255, 255))
        WIN.blit(retry_text, (WIDTH / 2 - retry_text.get_width() / 2, HEIGHT / 3 + 100))

        retry_options = [('YES', 150), ('NO', - 150)]
        for i, v in enumerate(retry_options, start=1):
            if i == active:
                label = TITLE_FONT.render(v[0], 1, (255, 0, 0))
            else:
                label = TITLE_FONT.render(v[0], 1, (255, 255, 255))
            WIN.blit(label, (WIDTH / 2 - label.get_width() / 2 - v[1], HEIGHT / 3 + 200))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if active == 2:
                        active = 1
                    else:
                        active += 1
                elif event.key == pygame.K_LEFT:
                    if active == 1:
                        active = 2
                    else:
                        active -= 1
                elif event.key == pygame.K_RETURN:
                    if active == 1:
                        main(WIN)
                    elif active == 2:
                        pygame.quit()
                        sys.exit()

def format_timer():
    mins = timer // 60
    formatted_mins = f'0{mins}' if mins < 10 else mins
    secs = timer - mins * 60
    formatted_secs = f'0{secs}' if secs < 10 else secs
    formatted_timer = f'{formatted_mins}:{formatted_secs}'

    return formatted_timer

def draw_next_shape(shape, surface, score):
    # draw preview next block
    text = PREVIEW_FONT.render('Next Block', 1, (255, 255, 255))

    preview_x = START_BOX_X + BOX_WIDTH + 50
    preview_y = START_BOX_Y + BOX_HEIGHT / 2 - 100
    surface.blit(text, (preview_x + 2.5 * BLOCK_SIZE - text.get_width() / 2, preview_y - 30 - BLOCK_SIZE))
    format = shape.shape[shape.rotation % len(shape.shape)]

    # draw score
    label = SCORE_FONT.render(f'SCORE: {score}', 1, (255, 255, 255))
    surface.blit(label, (preview_x + 2.5 * BLOCK_SIZE - label.get_width() / 2, preview_y - 80 - BLOCK_SIZE))

    # draw max score
    label = SCORE_FONT.render(f'MAX SCORE: {get_max_score()}', 1, (255, 255, 255))
    surface.blit(label, (START_BOX_X/2 - label.get_width()/2, preview_y - 80 - BLOCK_SIZE))

    # draw timer
    mins = timer // 60
    formatted_mins = f'0{mins}' if mins < 10 else mins
    secs = timer - mins * 60
    formatted_secs = f'0{secs}' if secs < 10 else secs
    label = SCORE_FONT.render(f'Timer {format_timer()}', 1, (255, 255, 255))
    surface.blit(label, (START_BOX_X/2 - label.get_width()/2, preview_y - 40))


    for i, row in enumerate(format):
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (preview_x + j * BLOCK_SIZE, preview_y + i * BLOCK_SIZE,
                                                        BLOCK_SIZE, BLOCK_SIZE), 0)
    # draw horizontal borders
    pygame.draw.line(surface, (255, 0, 0), (preview_x, preview_y - BLOCK_SIZE),
                     (preview_x + 5 * BLOCK_SIZE, preview_y - BLOCK_SIZE), width=3)
    pygame.draw.line(surface, (255, 0, 0), (preview_x, preview_y + 5 * BLOCK_SIZE),
                     (preview_x + 5 * BLOCK_SIZE, preview_y + 5 * BLOCK_SIZE), width=3)
    # draw vertical borders
    pygame.draw.line(surface, (255, 0, 0), (preview_x, preview_y - BLOCK_SIZE),
                     (preview_x, preview_y + 5 * BLOCK_SIZE), width=3)
    pygame.draw.line(surface, (255, 0, 0), (preview_x + 5 * BLOCK_SIZE, preview_y - BLOCK_SIZE),
                     (preview_x + 5 * BLOCK_SIZE, preview_y + 5 * BLOCK_SIZE), width=3)


def draw_menu_button(WIN, text, row, color, place=False):
    rows_height = {
        1: 150,
        2: 100,
        3: 50,
        4: 0,
        5: -50,
        6: -100,
        7: -150,
        8: -200,
        9: -250,
        10: -300
    }

    # mouse_x, mouse_y = pygame.mouse.get_pos()
    # label = PREVIEW_FONT.render(text, 1, (255, 255, 255))
    # button_x = WIDTH / 2 - label.get_width() / 2
    # if button_x < mouse_x < button_x + label.get_width() and HEIGHT / 2 - rows_height[row] < mouse_y < HEIGHT / 2 + rows_height[row]:
    #     label = PREVIEW_FONT.render(text, 1, (255, 0, 0))
    if place:
        label = PREVIEW_FONT.render(f'{str(row):^1}{text:^40}', 1, color)
    else:
        label = PREVIEW_FONT.render(text, 1, color)
    button_x = WIDTH / 2 - label.get_width() / 2
    WIN.blit(label, (button_x, HEIGHT / 2 - rows_height[row]))


def draw_menu(WIN, menu_title, buttons, highlight=True, place=False):
    menu_text = TITLE_FONT.render(menu_title, 1, (255, 255, 255))
    WIN.blit(menu_text, (WIDTH / 2 - menu_text.get_width() / 2, HEIGHT / 2 - 250))

    for i, v in enumerate(buttons, start=1):
        if i == active and highlight:
            draw_menu_button(WIN, v, i, (255, 0, 0))
        elif place:
            draw_menu_button(WIN, v, i, (255, 255, 255), place=True)
        else:
            draw_menu_button(WIN, v, i, (255, 255, 255))


def clear_rows(grid, lock):
    global extra_speed
    extra_speed = 0

    num_del = 0  # number of row to delete
    for i in range(len(grid) -1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            num_del += 1
            ind = i  # index of row to delete
            for j in range(len(row)):
                try:
                    del lock[(j, i)]
                except:
                    continue
    if num_del > 0:
        extra_speed += num_del
        for key in sorted(list(lock), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + num_del)
                lock[new_key] = lock.pop(key)

    return num_del


def pause(WIN):
    global active
    buttons = ['RESUME', 'RESTART', 'MAIN MENU', 'HIGH SCORES', 'EXIT']
    paused = True

    while paused:
        WIN.fill((0, 0, 0))
        draw_menu(WIN, 'PAUSE', buttons)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                elif event.key == pygame.K_DOWN:
                    if active == 5:
                        active = 1
                    else:
                        active += 1
                elif event.key == pygame.K_UP:
                    if active == 1:
                        active = 5
                    else:
                        active -= 1
                elif event.key == pygame.K_RETURN:
                    if active == 1:
                        paused = False
                    elif active == 2:
                        main(WIN)
                    elif active == 3:
                        main_menu(WIN)
                    elif active == 4:
                        get_leaderboard()
                    elif active == 5:
                        pygame.quit()
                        sys.exit()


def get_max_score():
    rows = []
    with open('scores.txt', 'r') as f:
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            rows.append(row[0])
    max_score = max(rows)
    return max_score


def save_score(score):
    with open('scores.txt', 'a+') as f:
        f.seek(0)
        data = f.read(100)
        if len(data) > 0:
            f.write('\n')
        f.write(f'{str(score)} {format_timer()}')


def get_leaderboard():
    rows = []
    with open('scores.txt', 'r') as f:
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            rows.append(row[0])
    leaderboard = sorted(rows, reverse=True)[:10]

    high_scores = True

    while high_scores:
        WIN.fill((0, 0, 0))
        draw_menu(WIN, 'LEADERBOARD', leaderboard, highlight=False, place=True)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    high_scores = False


def main(WIN):
    global timer
    locked_pos = {}
    grid = create_grid(locked_pos)
    speeds = [0.45, 0.3, 0.15]
    change_piece = False
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = speeds[speed]
    score = 0
    hardcore_time = 0
    time_elapsed = 0

    run = True
    while run:
        grid = create_grid(locked_pos)
        fall_time += clock.get_rawtime()
        time_elapsed += clock.get_rawtime()
        if mode == 2:
            hardcore_time += clock.get_rawtime()
        clock.tick()

        if time_elapsed / 1000 > 1:
            time_elapsed = 0
            timer += 1

        if hardcore_time / 1000 > 5:
            hardcore_time = 0
            if fall_speed > 0.1:
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                sys.exit()

            # Key handling
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                elif event.key == pygame.K_ESCAPE:
                    pause(WIN)

        shape_pos = convert_shape_format(current_piece)

        # draw square within the block
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_pos[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_pos) * 10
            if mode == 1 and fall_speed > 0.1:
                fall_speed -= extra_speed * 0.005

        draw_window(WIN, grid)
        draw_next_shape(next_piece, WIN, score)
        pygame.display.update()

        if check_lost(locked_pos):
            if score > 0:
                save_score(score)
            draw_lost_text(WIN)

    pygame.display.quit()


def main_menu(WIN):
    global active
    global speed
    global mode
    run = True
    speeds = ['LOW', 'MEDIUM', 'HIGH']
    modes = ['ENDLESS (CONSTANT SPEED)', 'SURVIVAL (INCREASING SPEED WHEN SCORING POINTS)',
             'HARDCORE (INCREASING SPEED OVER TIME)']
    while run:
        WIN.fill((0, 0, 0))
        buttons = ['NEW GAME', f'SPEED: {speeds[speed]}', f'MODE: {modes[mode]}', 'LEADERBOARD', 'EXIT']
        draw_menu(WIN, 'MAIN MENU', buttons)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if active == 5:
                        active = 1
                    else:
                        active += 1
                elif event.key == pygame.K_UP:
                    if active == 1:
                        active = 5
                    else:
                        active -= 1
                elif event.key == pygame.K_RETURN:
                    if active == 1:
                        main(WIN)
                    elif active == 2:
                        if speed == 2:
                            speed = 0
                        else:
                            speed += 1
                    elif active == 3:
                        if mode == 2:
                            mode = 0
                        else:
                            mode += 1
                    elif active == 4:
                        get_leaderboard()
                    elif active == 5:
                        pygame.quit()
                        sys.exit()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main_menu(WIN)
