import os
import matplotlib.pyplot as plt
from datetime import datetime
from constants import NUM_EPISODES


class Plotter:
    def __init__(self, plot_name):
        self.plot_dir = self.create_plot_directory()
        self.plot_name = plot_name

    def create_plot_directory(self):
        plot_dir = 'results/plots'
        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)
        return plot_dir

    def plot(self, rewards, steps):
        plt.figure(figsize=(12, 8))

        plt.subplot(2, 1, 1)
        plt.plot(rewards)
        plt.xlabel('Episódios')
        plt.ylabel('Recompensas')
        plt.title('Recompensas e Passos por Episódio')
        plt.grid(True)
        plt.xlim(0, NUM_EPISODES)

        plt.subplot(2, 1, 2)
        plt.plot(steps)
        plt.xlabel('Episódios')
        plt.ylabel('Passos')
        plt.grid(True)
        plt.xlim(0, NUM_EPISODES)
        plt.ylim(0)

        plt.tight_layout()
        plot_file = os.path.join(self.plot_dir, f'{self.plot_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
        plt.savefig(plot_file)
        plt.close()
