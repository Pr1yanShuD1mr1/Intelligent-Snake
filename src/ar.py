import torch
from random import randint
from collections import deque

from nn import deep_q_network, deep_q_trainer

class Agent:
    def __init__(self):
        import os
        
        self.memory = deque(maxlen=10**5)
        self.batchSize  = 1000

        model_file = "../model/dqn_model.pth"
        self.model  = deep_q_network(11,256,3)
        
        if os.path.exists(model_file):
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.load_state_dict(torch.load(model_file, map_location=device))

        self.engine = deep_q_trainer(self.model)





    def set_elipson(self, elipson):
        self.elipson = elipson

    def next_move(self, state):
        action = [0,0,0]    # left, straight, right

        if randint(1, 100) <= self.elipson:
            move = randint(0, 2)
            action[move] = 1
        else:
            state = torch.tensor(state, dtype=torch.float)
            out = self.model(state)
            move = torch.argmax(out).item()
            action[move] = 1

        return action





    def fit(self, old_state, action, reward, new_state, gameover):
        self.memory.append((old_state, action, reward, new_state, gameover))
        self.engine.fit(old_state, action, reward, new_state, gameover) # pending





    def learn(self):
        from random import sample
        if len(self.memory) > self.batchSize:
            mini_sample = sample(self.memory, self.batchSize) 
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.engine.fit(states, actions, rewards, next_states, dones)









