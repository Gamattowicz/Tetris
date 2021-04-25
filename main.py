import pygame
import random
import sys
from grid import create_grid, draw_grid
from score import get_score_factor, save_score, get_max_score
from leaderboard import get_leaderboard

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

# GLOBAL VARIABLES
active = 1
speed = 1
mode = 1
extra_speed = 0
timer = 0
speed_level = 30
start_speed_level = 30
combo = 0
max_combo = 0
fall_speed = 0.45 - start_speed_level * 0.005
start_fall_speed = 0.45 - start_speed_level * 0.005


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0


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
    title = TITLE_FONT.render('TETRIS', True, (255, 255, 255))
    surface.blit(title, (START_BOX_X + BOX_WIDTH / 2 - (title.get_width() / 2), 20))

    # draw each brick
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (START_BOX_X + j * BLOCK_SIZE, START_BOX_Y + i * BLOCK_SIZE,
                                                   BLOCK_SIZE, BLOCK_SIZE), 0)

    # draw border of box
    pygame.draw.rect(surface, (255, 0, 0), (START_BOX_X, START_BOX_Y, BOX_WIDTH, BOX_HEIGHT), 5)

    draw_grid(surface, grid, START_BOX_X, START_BOX_Y, BLOCK_SIZE, BOX_WIDTH, BOX_HEIGHT)


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
        lost_text = LOST_FONT.render('YOU LOST!', True, (255, 255, 255))
        WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 3))

        retry_text = TITLE_FONT.render('Do you want to play again?', True, (255, 255, 255))
        WIN.blit(retry_text, (WIDTH / 2 - retry_text.get_width() / 2, HEIGHT / 3 + 100))

        retry_options = [('YES', 150), ('NO', - 150)]
        for i, v in enumerate(retry_options, start=1):
            if i == active:
                label = TITLE_FONT.render(v[0], True, (255, 0, 0))
            else:
                label = TITLE_FONT.render(v[0], True, (255, 255, 255))
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
    text = PREVIEW_FONT.render('Next Block', True, (255, 255, 255))

    preview_x = START_BOX_X + BOX_WIDTH + 50
    preview_y = START_BOX_Y + BOX_HEIGHT / 2 - 100
    surface.blit(text, (preview_x + 2.5 * BLOCK_SIZE - text.get_width() / 2, preview_y - 30 - BLOCK_SIZE))
    format = shape.shape[shape.rotation % len(shape.shape)]

    # draw score
    label = SCORE_FONT.render(f'SCORE: {score}', True, (255, 255, 255))
    surface.blit(label, (preview_x + 2.5 * BLOCK_SIZE - label.get_width() / 2, preview_y - 80 - BLOCK_SIZE))

    # draw max score
    label = SCORE_FONT.render(f'MAX SCORE: {get_max_score() if get_max_score() else 0}', True, (255, 255, 255))
    surface.blit(label, (START_BOX_X/2 - label.get_width()/2, preview_y - 80 - BLOCK_SIZE))

    # draw timer
    label = SCORE_FONT.render(f'TIMER: {format_timer()}', True, (255, 255, 255))
    surface.blit(label, (START_BOX_X/2 - label.get_width()/2, preview_y - 40))

    # draw speed value
    label = SCORE_FONT.render(f'SPEED LEVEL: {speed_level}', True, (255, 255, 255))
    surface.blit(label, (START_BOX_X/2 - label.get_width()/2, preview_y + 30))

    # draw combo
    label = SCORE_FONT.render(f'COMBO: {combo}', True, (255, 255, 255))
    surface.blit(label, (START_BOX_X/2 - label.get_width()/2, preview_y + 100))

    # max combo
    label = SCORE_FONT.render(f'MAX COMBO: {max_combo}', True, (255, 255, 255))
    surface.blit(label, (START_BOX_X/2 - label.get_width()/2, preview_y + 170))

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


def draw_menu_button(WIN, text, row, color):
    rows_height = {
        1: 150,
        2: 100,
        3: 50,
        4: 0,
        5: -50
    }

    label = PREVIEW_FONT.render(text, True, color)
    button_x = WIDTH / 2 - label.get_width() / 2
    WIN.blit(label, (button_x, HEIGHT / 2 - rows_height[row]))


def draw_menu(WIN, menu_title, buttons):
    menu_text = TITLE_FONT.render(menu_title, True, (255, 255, 255))
    WIN.blit(menu_text, (WIDTH / 2 - menu_text.get_width() / 2, HEIGHT / 2 - 250))

    for i, v in enumerate(buttons, start=1):
        if i == active:
            draw_menu_button(WIN, v, i, (255, 0, 0))
        else:
            draw_menu_button(WIN, v, i, (255, 255, 255))


def clear_rows(grid, lock):
    global extra_speed
    global combo
    global max_combo
    extra_speed = 0

    num_del = 0  # number of row to delete
    for i in range(len(grid) - 1, -1, -1):
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
        combo += num_del
        max_combo = combo if combo > max_combo else max_combo
        for key in sorted(list(lock), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + num_del)
                lock[new_key] = lock.pop(key)
    else:
        combo = 0

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
                        restart_stats()
                        main(WIN)
                    elif active == 3:
                        main_menu(WIN)
                    elif active == 4:
                        get_leaderboard(WIN, WIDTH, HEIGHT)
                    elif active == 5:
                        pygame.quit()
                        sys.exit()


def restart_stats():
    global timer
    global speed_level
    global max_combo
    global fall_speed
    timer = 0
    max_combo = 0
    speed_level = start_speed_level
    fall_speed = start_fall_speed


def main(WIN):
    global timer
    global speed_level
    global fall_speed
    locked_pos = {}
    grid = create_grid(locked_pos)
    change_piece = False
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
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
                speed_level += 1

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
            score += clear_rows(grid, locked_pos) * get_score_factor(speed_level, combo)
            if mode == 1 and fall_speed > 0.1:
                fall_speed -= extra_speed * 0.005
                speed_level += extra_speed

        draw_window(WIN, grid)
        draw_next_shape(next_piece, WIN, score)
        pygame.display.update()

        if check_lost(locked_pos):
            if score > 0:
                save_score(score, format_timer(), speed_level, max_combo)
            restart_stats()
            draw_lost_text(WIN)

    pygame.display.quit()


def main_menu(WIN):
    global active
    global speed
    global mode
    global speed_level
    global start_speed_level
    global start_fall_speed
    global fall_speed
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
                        restart_stats()
                        main(WIN)
                    elif active == 2:
                        if speed == 2:
                            speed = 0
                            speed_level = 1
                            start_speed_level = 1
                            fall_speed = 0.45 - start_speed_level * 0.005
                            start_fall_speed = 0.45 - start_speed_level * 0.005
                        else:
                            speed += 1
                            speed_level += 30
                            start_speed_level += 30
                            fall_speed = 0.45 - start_speed_level * 0.005
                            start_fall_speed = 0.45 - start_speed_level * 0.005
                    elif active == 3:
                        if mode == 2:
                            mode = 0
                        else:
                            mode += 1
                    elif active == 4:
                        get_leaderboard(WIN, WIDTH, HEIGHT)
                    elif active == 5:
                        pygame.quit()
                        sys.exit()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main_menu(WIN)
