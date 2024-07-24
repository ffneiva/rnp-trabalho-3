import numpy as np
from constants import *


class Environment():
    def __init__(self):
        self.grid = np.zeros((GRID_SIZE + 2 * VIEW_RANGE, GRID_SIZE + 2 * VIEW_RANGE), dtype=int)
        self.reset()

    def reset(self):
        self.grid[VIEW_RANGE:GRID_SIZE + VIEW_RANGE, VIEW_RANGE:GRID_SIZE + VIEW_RANGE] = 0
        self.initial_position = (VIEW_RANGE, VIEW_RANGE)
        self.robot_position = self.initial_position
        self.treasure_position = (GRID_SIZE + VIEW_RANGE - 1, GRID_SIZE + VIEW_RANGE - 1)

        self.grid[0:VIEW_RANGE, :] = 1
        self.grid[GRID_SIZE + VIEW_RANGE:GRID_SIZE + 2 * VIEW_RANGE, :] = 1
        self.grid[:, 0:VIEW_RANGE] = 1
        self.grid[:, GRID_SIZE + VIEW_RANGE:GRID_SIZE + 2 * VIEW_RANGE] = 1

        self.generate_random_holes()
        self.grid[self.treasure_position[0], self.treasure_position[1]] = 3
        self.done = False
        return self.robot_position

    def step(self, action):
        if self.done:
            return self.robot_position, 0, True

        first_position = self.robot_position
        new_position = list(self.robot_position)
        
        if action == 0: # Direita
            new_position[1] += 1
        elif action == 1: # Esquerda
            new_position[1] -= 1
        elif action == 2: # Para cima
            new_position[0] -= 1
        elif action == 3: # Para baixo
            new_position[0] += 1

        self.robot_position = tuple(new_position)

        reward = self.calculate_reward(first_position)
        self.done = self.is_done()

        return self.robot_position, reward, self.done

    def generate_random_holes(self):
        num_holes = np.random.randint(MIN_HOLES, MAX_HOLES + 1)
        hole_positions = []
        while len(hole_positions) < num_holes:
            hole_position = tuple(np.random.randint(VIEW_RANGE, GRID_SIZE + VIEW_RANGE, size=2))
            if (hole_position != self.robot_position and
                hole_position != self.treasure_position and
                hole_position not in hole_positions):
                self.grid[hole_position[0], hole_position[1]] = 2
                hole_positions.append(hole_position)
        self.hole_positions = hole_positions

    def calculate_reward(self, first_position):
        first_distance = np.sqrt((first_position[0] - self.treasure_position[0]) ** 2 + (first_position[1] - self.treasure_position[1]) ** 2)
        current_distance = np.sqrt((self.robot_position[0] - self.treasure_position[0]) ** 2 + (self.robot_position[1] - self.treasure_position[1]) ** 2)

        if (self.robot_position[0] < VIEW_RANGE or self.robot_position[0] >= GRID_SIZE + VIEW_RANGE or
            self.robot_position[1] < VIEW_RANGE or self.robot_position[1] >= GRID_SIZE + VIEW_RANGE):
            return REWARD_EDGE
        elif self.robot_position in self.hole_positions:
            return REWARD_HOLE
        elif self.robot_position == self.treasure_position:
            return REWARD_TREASURE
        else:
            if current_distance < first_distance:
                return REWARD_MOVE
            elif current_distance > first_distance:
                return - REWARD_MOVE
            else:
                return - REWARD_MOVE / 2

    def is_done(self):
        if self.robot_position == self.treasure_position:
            return True
        elif self.robot_position in self.hole_positions:
            return True
        if (self.robot_position[0] < VIEW_RANGE or self.robot_position[0] >= GRID_SIZE + VIEW_RANGE or
            self.robot_position[1] < VIEW_RANGE or self.robot_position[1] >= GRID_SIZE + VIEW_RANGE):
            return True

        return False

    def get_state(self, robot_position):
        size = VIEW_RANGE * 2 + 1
        state = np.ones((size, size))
        top_left_x = robot_position[0] - VIEW_RANGE
        top_left_y = robot_position[1] - VIEW_RANGE
        bottom_right_x = robot_position[0] + VIEW_RANGE + 1
        bottom_right_y = robot_position[1] + VIEW_RANGE + 1

        try:
            subgrid = self.env.grid[top_left_x:bottom_right_x, top_left_y:bottom_right_y]
            state[subgrid == 3] = 1 + GRID_SIZE + VIEW_RANGE
            state[subgrid == 1] = -1
            state[subgrid == 2] = -1
        except:
            subgrid = np.zeros((size, size))

        return np.append(state.flatten(), robot_position) / (1 + GRID_SIZE + VIEW_RANGE)
