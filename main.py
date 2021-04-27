import pygame
import random
import sys
from grid import create_grid, draw_grid
from player import Player
from leaderboard import get_leaderboard
from menu import draw_menu, pause
from validation import valid_space, check_lost
from game_window import draw_window, draw_next_shape

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
mode = 1


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


def draw_name(win, player):
    draw = True
    while draw:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    player.name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    player.name = player.name[:-1]
                elif event.key == pygame.K_RETURN or event.type == pygame.QUIT:
                    draw = False
        win.fill((0, 0, 0))

        lost_text = LOST_FONT.render('YOU LOST!', True, (255, 255, 255))
        WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 10))

        input_text = TITLE_FONT.render('Enter your name:', True, (255, 255, 255))
        WIN.blit(input_text, (WIDTH / 2 - input_text.get_width() / 2, HEIGHT / 4 + 50))

        block = PREVIEW_FONT.render(player.name, True, (255, 255, 255))
        rect = block.get_rect()
        rect.center = win.get_rect().center
        win.blit(block, rect)
        pygame.display.update()

    if player.score > 0:
        player.save_score(player.format_timer)
    player.restart_stats()
    draw_lost_text(WIN, player)


def draw_lost_text(WIN, player):
    global active
    lost = True

    while lost:
        WIN.fill((0, 0, 0))

        retry_text = TITLE_FONT.render('Do you want to play again?', True, (255, 255, 255))
        WIN.blit(retry_text, (WIDTH / 2 - retry_text.get_width() / 2, HEIGHT / 5))

        retry_options = [('YES', 150), ('NO', - 150)]
        for i, v in enumerate(retry_options, start=1):
            if i == active:
                label = TITLE_FONT.render(v[0], True, (255, 0, 0))
            else:
                label = TITLE_FONT.render(v[0], True, (255, 255, 255))
            WIN.blit(label, (WIDTH / 2 - label.get_width() / 2 - v[1], HEIGHT / 3 + 100))
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
                        main(WIN, player)
                    elif active == 2:
                        pygame.quit()
                        sys.exit()


def clear_rows(grid, lock, player):
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
        player.extra_speed += num_del
        player.combo += num_del
        player.max_combo = player.combo if player.combo > player.max_combo else player.max_combo
        if mode == 1 and player.fall_speed > 0.1:
            player.fall_speed -= player.extra_speed * 0.005
            player.speed_level += player.extra_speed
        for key in sorted(list(lock), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + num_del)
                lock[new_key] = lock.pop(key)
    else:
        player.combo = 0

    return num_del


def main(WIN, player):
    locked_pos = {}
    grid = create_grid(locked_pos)
    change_piece = False
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    hardcore_time = 0
    time_elapsed = 0

    player.restart_stats()

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
            player.timer += 1

        if hardcore_time / 1000 > 5:
            hardcore_time = 0
            if player.fall_speed > 0.1:
                player.fall_speed -= 0.005
                player.speed_level += 1

        if fall_time / 1000 > player.fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid, convert_shape_format)) and current_piece.y > 0:
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
                    if not (valid_space(current_piece, grid, convert_shape_format)):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid, convert_shape_format)):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid, convert_shape_format)):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid, convert_shape_format)):
                        current_piece.rotation -= 1
                elif event.key == pygame.K_RETURN:
                    for i in range(20):
                        current_piece.y += 1
                        if not (valid_space(current_piece, grid, convert_shape_format)):
                            current_piece.y -= 1
                elif event.key == pygame.K_ESCAPE:
                    pause(WIN, active, WIDTH, HEIGHT, player.restart_stats, main, main_menu, get_leaderboard, player)

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
            player.score += clear_rows(grid, locked_pos, player) * player.get_score_factor()

        draw_window(WIN, grid, START_BOX_X, START_BOX_Y, BOX_WIDTH, BOX_HEIGHT, BLOCK_SIZE, draw_grid)
        draw_next_shape(next_piece, WIN, player.score, START_BOX_X, START_BOX_Y, BOX_WIDTH, BOX_HEIGHT, BLOCK_SIZE,
                        player.get_max_score, player.format_timer, player.speed_level, player.combo, player.max_combo)
        pygame.display.update()

        if check_lost(locked_pos):
            draw_name(WIN, player)

    pygame.display.quit()


def main_menu(WIN):
    global active
    global mode
    player = Player()
    run = True
    speeds = ['LOW', 'MEDIUM', 'HIGH']
    modes = ['ENDLESS (CONSTANT SPEED)', 'SURVIVAL (INCREASING SPEED WHEN SCORING POINTS)',
             'HARDCORE (INCREASING SPEED OVER TIME)']
    while run:
        WIN.fill((0, 0, 0))
        buttons = ['NEW GAME', f'SPEED: {speeds[player.speed]}', f'MODE: {modes[mode]}', 'LEADERBOARD', 'EXIT']
        draw_menu(WIN, 'MAIN MENU', buttons, WIDTH, HEIGHT, active)
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
                        main(WIN, player)
                    elif active == 2:
                        if player.speed == 2:
                            player.speed = 0
                            player.speed_level = 1
                            player.start_speed_level = 1
                            player.fall_speed = 0.45 - player.start_speed_level * 0.005
                            player.start_fall_speed = 0.45 - player.start_speed_level * 0.005
                        else:
                            player.speed += 1
                            player.speed_level += 30
                            player.start_speed_level += 30
                            player.fall_speed = 0.45 - player.start_speed_level * 0.005
                            player.start_fall_speed = 0.45 - player.start_speed_level * 0.005
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
