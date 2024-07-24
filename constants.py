import os
import pygame


# Dimensões e Tamanhos
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 50
CELL_SIZE = 100
GRID_SIZE = 5
WINDOW_HEIGHT_OFFSET = 100
WINDOW_SIZE = (GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE + WINDOW_HEIGHT_OFFSET)

# Posições dos Botões
PLAY_BUTTON_RECT = pygame.Rect((WINDOW_SIZE[0] // 2) - BUTTON_WIDTH - 10, GRID_SIZE * CELL_SIZE + 20, BUTTON_WIDTH, BUTTON_HEIGHT)
RESTART_BUTTON_RECT = pygame.Rect((WINDOW_SIZE[0] // 2) + 10, GRID_SIZE * CELL_SIZE + 20, BUTTON_WIDTH, BUTTON_HEIGHT)

# Campo de visão do robô
VIEW_RANGE = 1

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (40, 40, 40)
GREEN = (0, 128, 0)
RED = (128, 0, 0)
BLUE = (0, 0, 128)

# Recompensas
REWARD_EDGE = -5
REWARD_HOLE = -5
REWARD_MOVE = 0.5
REWARD_TREASURE = 5

# Episódios de treinamento
NUM_EPISODES = 500

# Quantidade de buracos
MIN_HOLES = 1
MAX_HOLES = 3

# Carregamento de Imagens
ROBOT_IMAGE = pygame.image.load(os.path.join('assets/images', 'robot.png'))
ROBOT_IMAGE = pygame.transform.scale(ROBOT_IMAGE, (CELL_SIZE, CELL_SIZE))
HOLE_IMAGE = pygame.image.load(os.path.join('assets/images', 'hole.png'))
HOLE_IMAGE = pygame.transform.scale(HOLE_IMAGE, (CELL_SIZE, CELL_SIZE))
TREASURE_IMAGE = pygame.image.load(os.path.join('assets/images', 'treasure.png'))
TREASURE_IMAGE = pygame.transform.scale(TREASURE_IMAGE, (CELL_SIZE, CELL_SIZE))
