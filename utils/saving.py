import torch
import os
from datetime import datetime


class Saver:
    def __init__(self, model_name):
        self.plot_dir = self.create_plot_directory()
        self.model_name = model_name

    def create_plot_directory(self):
        plot_dir = 'results/models'
        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)
        return plot_dir

    def save_model(self, net):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        net_path = os.path.join(self.plot_dir, f'{self.model_name}_net_{timestamp}.pt')

        torch.save(net.state_dict(), net_path)

    def load_model(self):
        model_files = [f for f in os.listdir(self.plot_dir) if f.startswith(self.model_name)]
        if not model_files:
            return None, None

        latest_net_file = max([f for f in model_files if 'net' in f], key=lambda f: os.path.getctime(os.path.join(self.plot_dir, f)))
        net_path = os.path.join(self.plot_dir, latest_net_file)
        net_state_dict = torch.load(net_path)

        return net_state_dict
