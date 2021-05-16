import pygame
import sys
from board import TITLE_FONT, SCORE_FONT, BACKGROUND_COLOR, TEXT_COLOR

pygame.font.init()

ACTIVE_COLOR = (234, 113, 134)


def draw_menu_button(win, text, row, color, width, height):
    rows_height = {
        1: 150,
        2: 100,
        3: 50,
        4: 0,
        5: -50
    }

    label = SCORE_FONT.render(text, True, color)
    button_x = width / 2 - label.get_width() / 2
    win.blit(label, (button_x, height / 2 - rows_height[row]))


def draw_menu(win, menu_title, buttons, width, height, active):
    menu_text = TITLE_FONT.render(menu_title, True, TEXT_COLOR)
    win.blit(menu_text, (width / 2 - menu_text.get_width() / 2, height / 2 - 250))

    for i, v in enumerate(buttons, start=1):
        if i == active:
            draw_menu_button(win, v, i, ACTIVE_COLOR, width, height)
        else:
            draw_menu_button(win, v, i, TEXT_COLOR, width, height)


def pause(win, active, width, height, restart, main, main_menu, get_leaderboard, player):
    buttons = ['RESUME', 'RESTART', 'MAIN MENU', 'HIGH SCORES', 'EXIT']
    paused = True

    while paused:
        win.fill(BACKGROUND_COLOR)
        draw_menu(win, 'PAUSE', buttons, width, height, active)
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
                        restart()
                        main(win, player)
                    elif active == 3:
                        main_menu(win)
                    elif active == 4:
                        get_leaderboard(win, width, height)
                    elif active == 5:
                        pygame.quit()
                        sys.exit()