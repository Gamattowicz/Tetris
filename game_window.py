import pygame

pygame.font.init()

TITLE_FONT = pygame.font.SysFont('arial', 60)
SCORE_FONT = pygame.font.SysFont('arial', 25)
SHAPE_FONT = pygame.font.SysFont('arial', 20)

BACKGROUND_COLOR = (11, 12, 16)


def draw_window(surface, grid, start_x, start_y, width, height, block_size, draw_grid):
    surface.fill(BACKGROUND_COLOR)

    # draw title over the box
    title = TITLE_FONT.render('TETRIS', True, (255, 255, 255))
    surface.blit(title, (start_x + width / 2 - (title.get_width() / 2), 20))

    # draw each brick
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (start_x + j * block_size, start_y + i * block_size,
                                                   block_size, block_size), 0)

    # draw border of box
    pygame.draw.rect(surface, (255, 0, 0), (start_x, start_y, width, height), 5)

    draw_grid(surface, grid, start_x, start_y, block_size, width, height)


def draw_next_shape(shape, surface, score, start_x, start_y, width, height, block_size, get_max_score, format_timer,
                    speed_level, combo, max_combo):
    # draw preview next block
    text = SHAPE_FONT.render('Next Block', True, (255, 255, 255))

    preview_x = start_x + width + 50
    preview_y = start_y + height / 2 - 100
    surface.blit(text, (preview_x + 2.5 * block_size - text.get_width() / 2, preview_y - 30 - block_size))
    format = shape.shape[shape.rotation % len(shape.shape)]

    # draw score
    label = SCORE_FONT.render(f'SCORE: {score}', True, (255, 255, 255))
    surface.blit(label, (preview_x + 2.5 * block_size - label.get_width() / 2, preview_y - 80 - block_size))

    # draw max score
    label = SCORE_FONT.render(f'MAX SCORE: {get_max_score() if get_max_score() else 0}', True, (255, 255, 255))
    surface.blit(label, (start_x/2 - label.get_width()/2, preview_y - 80 - block_size))

    # draw timer
    label = SCORE_FONT.render(f'TIMER: {format_timer()}', True, (255, 255, 255))
    surface.blit(label, (start_x/2 - label.get_width()/2, preview_y - 40))

    # draw speed value
    label = SCORE_FONT.render(f'SPEED LEVEL: {speed_level}', True, (255, 255, 255))
    surface.blit(label, (start_x/2 - label.get_width()/2, preview_y + 30))

    # draw combo
    label = SCORE_FONT.render(f'COMBO: {combo}', True, (255, 255, 255))
    surface.blit(label, (start_x/2 - label.get_width()/2, preview_y + 100))

    # max combo
    label = SCORE_FONT.render(f'MAX COMBO: {max_combo}', True, (255, 255, 255))
    surface.blit(label, (start_x/2 - label.get_width()/2, preview_y + 170))

    for i, row in enumerate(format):
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (preview_x + j * block_size, preview_y + i * block_size,
                                                        block_size, block_size), 0)
    # draw horizontal borders
    pygame.draw.line(surface, (255, 0, 0), (preview_x, preview_y - block_size),
                     (preview_x + 5 * block_size, preview_y - block_size), width=3)
    pygame.draw.line(surface, (255, 0, 0), (preview_x, preview_y + 5 * block_size),
                     (preview_x + 5 * block_size, preview_y + 5 * block_size), width=3)
    # draw vertical borders
    pygame.draw.line(surface, (255, 0, 0), (preview_x, preview_y - block_size),
                     (preview_x, preview_y + 5 * block_size), width=3)
    pygame.draw.line(surface, (255, 0, 0), (preview_x + 5 * block_size, preview_y - block_size),
                     (preview_x + 5 * block_size, preview_y + 5 * block_size), width=3)