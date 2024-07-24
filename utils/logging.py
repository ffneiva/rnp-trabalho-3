import os
import csv
from datetime import datetime

from constants import *


class Logger:
    def __init__(self, log_name):
        self.log_dir = 'results/logs'
        self.log_name = log_name
        self.log_file = self.create_log_file()
        self.setup_logging()

    def create_log_file(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.log_dir, f'{self.log_name}_{timestamp}.csv')

    def setup_logging(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        self.csv = open(self.log_file, mode='w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv)
        self.csv_writer.writerow(['Episódio', 'Tamanho', 'Visão', 'Robô', 'Tesouro', 'Buracos', 'Recompensa', 'Passos', 'Ações', 'Estados'])

    def log_episode(self, episode, robot, treasure, holes, reward, steps, actions, states):
        log_entry = [episode, GRID_SIZE, VIEW_RANGE, robot, treasure, holes, reward, steps, actions, states]
        self.csv_writer.writerow(log_entry)

    def list_log_files(self):
        log_files = [os.path.join(self.log_dir, f) for f in os.listdir(self.log_dir) if f.endswith('.csv') and self.log_name in f]
        log_files.sort(key=os.path.getmtime, reverse=True)
        return log_files

    def get_latest_log_file(self):
        log_files = self.list_log_files()
        return log_files[0] if log_files else None

    def __del__(self):
        if hasattr(self, 'csv') and not self.csv.closed:
            self.csv.close()
