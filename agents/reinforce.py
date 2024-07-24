import csv
import pygame
import torch
import torch.nn as nn
from torch.distributions import Categorical
from tqdm import tqdm
from environment.env import Environment
from constants import *
from interface.gui import draw_buttons, draw_environment
from utils.logging import Logger
from utils.plotting import Plotter
from utils.saving import Saver


class Reinforce:
    def __init__(self, lr=0.01, gamma=0.99, qtd_passos=50):
        self.logger = Logger('reinforce')
        self.plotter = Plotter('reinforce')
        self.saver = Saver('reinforce')
        self.env = Environment()
        # self.gui = GUI(self.env, self.logger, title='REINFORCE')
        self.lr = lr
        self.gamma = gamma
        self.qtd_passos = qtd_passos
        input_dim = (VIEW_RANGE * 2 + 1) ** 2 + 2  # Campo de visão + posição do robô
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128), nn.LeakyReLU(),
            nn.Linear(128, 256), nn.LeakyReLU(),
            nn.Linear(256, 128), nn.LeakyReLU(),
            nn.Linear(128, 64), nn.LeakyReLU(),
            nn.Linear(64, 4), nn.Softmax(dim=-1)
        )
        try:
            net_state_dict = self.saver.load_model()
            if net_state_dict:
                self.net.load_state_dict(net_state_dict)
        except:
            print('Não foi possível carregar um modelo REINFORCE.')
        self.trainer = torch.optim.SGD(self.net.parameters(), lr=self.lr)

    def choose_action(self, state):
        state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        probs = self.net(state_tensor)
        pd = Categorical(probs)
        action = pd.sample()
        return action.item(), pd.log_prob(action)

    def train(self, episodes=1000):
        rewards_per_episode = []
        steps_per_episode = []

        for episode in tqdm(range(episodes)):
            robot_position = self.env.reset()
            state = self.env.get_state(robot_position)
            rewards = []
            log_probs = []
            states = [robot_position]

            for t in range(self.qtd_passos):
                previous_state = state
                action, log_prob = self.choose_action(previous_state)
                next_robot_position, reward, done = self.env.step(action)
                state = self.env.get_state(next_robot_position)

                rewards.append(reward)
                log_probs.append(log_prob)
                states.append(next_robot_position)

                if done:
                    break

            returns = []
            ret = 0
            for reward in reversed(rewards):
                ret = reward + self.gamma * ret
                returns.append(ret)
            returns = list(reversed(returns))

            loss = 0
            for log_prob, ret in zip(log_probs, returns):
                loss -= log_prob * ret

            self.trainer.zero_grad()
            loss.backward()
            self.trainer.step()

            rewards_per_episode.append(sum(rewards))
            steps_per_episode.append(len(rewards))
            self.logger.log_episode(episode + 1, self.env.initial_position, self.env.treasure_position, [tuple(p) for p in self.env.hole_positions], sum(rewards), len(rewards), None, states)

        self.plotter.plot(rewards_per_episode, steps_per_episode)
        self.saver.save_model(self.net)

    def find_latest_log_file(self):
        log_files = [f for f in os.listdir('results/logs') if f.startswith('reinforce') and f.endswith('.csv')]
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
        pygame.display.set_caption('REINFORCE')
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
