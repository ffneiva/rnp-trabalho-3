from agents.sarsa import Sarsa
from agents.reinforce import Reinforce
from constants import *

def main():
    sarsa_agent = Sarsa()
    reinforce_agent = Reinforce()

    sarsa_agent.train(NUM_EPISODES)
    states = sarsa_agent.test()
    sarsa_agent.render(states)

    reinforce_agent.train(NUM_EPISODES)
    states = reinforce_agent.test()
    reinforce_agent.render(states)

if __name__ == "__main__":
    main()
