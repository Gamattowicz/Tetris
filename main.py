import pygame
import random

# SIZE OF SCREEN
WIDTH, HEIGHT = 800, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TETRIS')
pygame.init()

# SIZE OF BOX
BLOCK_SIZE = 30
BOX_WIDTH, BOX_HEIGHT = 10 * BLOCK_SIZE, 20 * BLOCK_SIZE

# BEGIN POINT OF BOX
START_BOX_X = (WIDTH - BOX_WIDTH) // 2
START_BOX_Y = HEIGHT - BOX_HEIGHT

# FONTS
TITLE_FONT = pygame.font.SysFont('arial', 60)

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
        pygame.draw.line(surface, (128,128,128), (START_BOX_X, START_BOX_Y + i * BLOCK_SIZE), (START_BOX_X + BOX_WIDTH,
                                                                                              START_BOX_Y + i * BLOCK_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (START_BOX_X + j * BLOCK_SIZE, START_BOX_Y), (START_BOX_X + j * BLOCK_SIZE,
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
    pygame.display.update()


def main(WIN):
    locked_pos = {}
    grid = create_grid(locked_pos)

    change_piece = False
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27

    run = True
    while run:
        grid = create_grid(locked_pos)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

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

        draw_window(WIN, grid)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main(WIN)