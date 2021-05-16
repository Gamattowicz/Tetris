import pygame
from board import FRAME_COLOR

GRID_COLOR = FRAME_COLOR
BLOCK_COLOR = (250, 210, 204)


def create_grid(locked_pos={}):
    grid = [[BLOCK_COLOR for i in range(10)] for i in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


def draw_grid(surface, grid, start_x, start_y, block_size, width, height):
    for i in range(len(grid)):
        pygame.draw.line(surface, GRID_COLOR, (start_x, start_y + i * block_size),
                         (start_x + width, start_y + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, GRID_COLOR, (start_x + j * block_size, start_y),
                             (start_x + j * block_size, start_y + height))