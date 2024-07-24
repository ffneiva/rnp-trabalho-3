import csv
import numpy as np
import torch
import torch.nn as nn
from tqdm import tqdm
from environment.env import Environment
from constants import *
from interface.gui import draw_buttons, draw_environment
from utils.logging import Logger
from utils.plotting import Plotter
from utils.saving import Saver


class Sarsa:
    def __init__(self, epsilon=0.2, lr=0.001, gamma=0.99, qtd_passos=50):
        self.logger = Logger('sarsa')
        self.plotter = Plotter('sarsa')
        self.saver = Saver('sarsa')
        self.env = Environment()
        # self.gui = GUI(self.env, self.logger, title='SARSA')
        self.epsilon = epsilon
        self.lr = lr
        self.gamma = gamma
        self.qtd_passos = qtd_passos
        input_dim = (VIEW_RANGE * 2 + 1) ** 2 + 2  # Campo de visão + posição do robô
        self.net = nn.Sequential(nn.Linear(input_dim, 128), nn.ReLU(),
                                nn.Linear(128, 256), nn.ReLU(),
                                nn.Linear(256, 128), nn.ReLU(),
                                nn.Linear(128, 4))
        try:
            net_state_dict = self.saver.load_model()
            if net_state_dict:
                self.net.load_state_dict(net_state_dict)
        except:
            print('Não foi possível carregar um modelo SARSA.')
        self.trainer = torch.optim.SGD(self.net.parameters(), lr=self.lr, weight_decay=0.1)
        self.loss_fn = nn.MSELoss()

    def choose_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.choice(4)
        else:
            state_tensor = torch.tensor(state, dtype=torch.float32)
            q_values = self.net(state_tensor)
            return torch.argmax(q_values).item()

    def train(self, episodes=1000):
        rewards_per_episode = []
        steps_per_episode = []

        for episode in tqdm(range(episodes)):
            robot_position = self.env.reset()
            state = self.env.get_state(robot_position)
            rewards = []
            actions = []
            states = [robot_position]

            for t in range(self.qtd_passos):
                previous_state = state
                action = self.choose_action(previous_state)

                next_robot_position, reward, done = self.env.step(action)
                state = self.env.get_state(next_robot_position)
                next_action = self.choose_action(state)

                state_tensor = torch.tensor(previous_state, dtype=torch.float32)
                next_state_tensor = torch.tensor(state, dtype=torch.float32)

                q_value = self.net(state_tensor)[action]
                next_q_value = self.net(next_state_tensor)[next_action]

                target = reward + self.gamma * next_q_value * (1 - int(done))
                loss = self.loss_fn(q_value, target)

                self.trainer.zero_grad()
                loss.backward()
                self.trainer.step()

                rewards.append(reward)
                actions.append(action)
                states.append(next_robot_position)

                if done:
                    break
            self.epsilon = max(0.01, 0.999 * self.epsilon)

            rewards_per_episode.append(sum(rewards))
            steps_per_episode.append(len(actions))
            self.logger.log_episode(episode + 1, self.env.initial_position, self.env.treasure_position, [tuple(p) for p in self.env.hole_positions], sum(rewards), len(actions), actions, states)

        self.plotter.plot(rewards_per_episode, steps_per_episode)
        self.saver.save_model(self.net)

    def find_latest_log_file(self):
        log_files = [f for f in os.listdir('results/logs') if f.startswith('sarsa') and f.endswith('.csv')]
        if not log_files:
            return None
        latest_log_file = max(log_files, key=lambda f: os.path.getctime(os.path.join('results/logs', f)))
        return os.path.join('results/logs', latest_log_file)

    def find_best_episode_states(self, log_file):
        best_reward = float('-inf')
        best_states = None

        with open(log_file, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                reward = float(row['Recompensa'])
                if reward > best_reward:
                    best_reward = reward
                    best_states = eval(row['Estados'])

        return best_states

    def test(self):
        log_file = self.find_latest_log_file()
        if not log_file:
            return []

        best_states = self.find_best_episode_states(log_file)
        if not best_states:
            return []

        return best_states

    def render(self, states):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption('SARSA')
        pygame.display.set_icon(ROBOT_IMAGE)

        running = True
        execute_trajectory = False
        current_step = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON_RECT.collidepoint(event.pos):
                        execute_trajectory = True
                        current_step = 0
                    elif RESTART_BUTTON_RECT.collidepoint(event.pos):
                        states = self.test()
                        execute_trajectory = True
                        current_step = 0

            if execute_trajectory and current_step < len(states):
                robot_position = states[current_step]
                draw_environment(self.screen, self.env, robot_position)
                draw_buttons(self.screen)
                pygame.display.update()
                pygame.time.delay(500)
                current_step += 1
            else:
                draw_environment(self.screen, self.env, states[-1] if states else self.env.reset())
                draw_buttons(self.screen)
                pygame.display.update()

        pygame.quit()
