from grid import BLOCK_COLOR


def valid_space(shape, grid, convert_shape_format):
    free_pos = [[(j, i) for j in range(10) if grid[i][j] == BLOCK_COLOR] for i in range(20)]
    free_pos = [j for sub in free_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in free_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False
