import torch
import torch.nn as nn
import torch.optim as optim





class deep_q_network(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(deep_q_network, self).__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.relu    = nn.ReLU()
        self.linear2 = nn.Linear(hidden_size, output_size)



    def forward(self, x):
        out = self.linear1(x)
        out = self.relu(out)
        out = self.linear2(out)
        return out



    def save(self, saved_as="../model/dqn_model.pth"):
        torch.save(self.state_dict(), saved_as)
         





    


class deep_q_trainer:
    def __init__(self, neuralmodel, learningRate=0.001, gamma=0.9):
        self.neuralmodel = neuralmodel
        self.optimizer = optim.Adam(neuralmodel.parameters(), lr=learningRate)
        self.criterion = nn.MSELoss()
        self.gamma = gamma

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")            
        self.neuralmodel = neuralmodel.to(self.device)

  

  

    def fit(self, old_state, action, reward, new_state, gameover):
            old_state = torch.tensor(old_state, dtype=torch.float)
            new_state = torch.tensor(new_state, dtype=torch.float)
            action    = torch.tensor(action, dtype=torch.long)
            reward    = torch.tensor(reward, dtype=torch.float)

            if len(old_state.shape) == 1:
                old_state = torch.unsqueeze(old_state, 0)
                new_state = torch.unsqueeze(new_state, 0)
                action = torch.unsqueeze(action, 0)
                reward = torch.unsqueeze(reward, 0)
                gameover = (gameover, ) # Make it iterable

            gameover = torch.tensor(gameover, dtype=torch.float)

            prediction = self.neuralmodel(old_state)            
            target = prediction.clone().detach()

            with torch.no_grad():
                next_prediction = self.neuralmodel(new_state)
                max_next_prediction = torch.max(next_prediction, dim=1)[0]

            Q_new = reward + self.gamma * max_next_prediction * (1 - gameover)

            action_indices = torch.argmax(action, dim=1)
            batch_indices = torch.arange(len(gameover))
            target[batch_indices, action_indices] = Q_new

            self.optimizer.zero_grad()            
            loss = self.criterion(prediction, target) 
            loss.backward()
            self.optimizer.step()




