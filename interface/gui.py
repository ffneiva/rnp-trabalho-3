import pygame
from constants import *


def draw_environment(screen, env, robot_position):
    screen.fill(WHITE)

    for hole_pos in env.hole_positions:
        hole_rect = HOLE_IMAGE.get_rect()
        hole_rect.topleft = ((hole_pos[1] - VIEW_RANGE) * CELL_SIZE, (hole_pos[0] - VIEW_RANGE) * CELL_SIZE)
        screen.blit(HOLE_IMAGE, hole_rect)

    treasure_rect = TREASURE_IMAGE.get_rect()
    treasure_rect.topleft = ((env.treasure_position[1] - VIEW_RANGE) * CELL_SIZE, (env.treasure_position[0] - VIEW_RANGE) * CELL_SIZE)
    screen.blit(TREASURE_IMAGE, treasure_rect)

    robot_rect = ROBOT_IMAGE.get_rect()
    robot_rect.topleft = ((robot_position[1] - VIEW_RANGE) * CELL_SIZE, (robot_position[0] - VIEW_RANGE) * CELL_SIZE)
    screen.blit(ROBOT_IMAGE, robot_rect)

    for x in range(GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x * CELL_SIZE, 0), (x * CELL_SIZE, GRID_SIZE * CELL_SIZE))
        pygame.draw.line(screen, BLACK, (0, x * CELL_SIZE), (GRID_SIZE * CELL_SIZE, x * CELL_SIZE))
    pygame.draw.line(screen, BLACK, (0, GRID_SIZE * CELL_SIZE), (GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))

    if VIEW_RANGE:
        pygame.draw.rect(screen, BLUE, ((robot_position[1] - VIEW_RANGE) * CELL_SIZE - VIEW_RANGE * CELL_SIZE,
                                        (robot_position[0] - VIEW_RANGE) * CELL_SIZE - VIEW_RANGE * CELL_SIZE,
                                        (2 * VIEW_RANGE + 1) * CELL_SIZE, (2 * VIEW_RANGE + 1) * CELL_SIZE), 2)


def draw_buttons(screen):
    font = pygame.font.Font(None, 30)

    pygame.draw.rect(screen, GREEN, PLAY_BUTTON_RECT, border_radius=10)
    play_text = font.render('Iniciar', True, WHITE)
    text_rect = play_text.get_rect(center=PLAY_BUTTON_RECT.center)
    screen.blit(play_text, text_rect)
    
    pygame.draw.rect(screen, RED, RESTART_BUTTON_RECT, border_radius=10)
    restart_text = font.render('Reiniciar', True, WHITE)
    text_rect = restart_text.get_rect(center=RESTART_BUTTON_RECT.center)
    screen.blit(restart_text, text_rect)
