import torch
import torch.nn as nn
import numpy as np

def fanin_init(size, fanin=None):
    fanin = fanin or size[0]
    v = 1. / np.sqrt(fanin)
    return torch.Tensor(size).uniform_(-v, v)

class Critic(nn.Module):

    def __init__(self,
                 observation_dims: int,
                 action_dims: int,
                 hidden_size: int,
                 activation: str):
        
        super(Critic, self).__init__()
        self.__observation_dims = observation_dims
        self.__action_dims = action_dims

        activation_layer = None
        if activation == 'relu':
            activation_layer = nn.ReLU()
        elif activation == 'tanh':
            activation_layer = nn.Tanh()
        else:
            raise NotImplementedError("Activation layer {} is not Supported yet.".format(activation))

        self.fc1 = nn.Linear(out_features=hidden_size, in_features=observation_dims + action_dims)
        self.fc2 = nn.Linear(out_features=hidden_size, in_features=hidden_size)
        self.fc3 = nn.Linear(out_features=1, in_features=hidden_size)
        self.activation = activation_layer
        self.init_weights(init_w=3e-3)
        
    def init_weights(self, init_w):
        self.fc1.weight.data = fanin_init(self.fc1.weight.data.size())
        self.fc2.weight.data = fanin_init(self.fc2.weight.data.size())
        self.fc3.weight.data.uniform_(-init_w, init_w)

    @property
    def observation_dims(self):
        return self.__observation_dims

    @property
    def action_dims(self):
        return self.__action_dims
    
    def forward(self,
                states: torch.FloatTensor,
                actions: torch.FloatTensor):
        
        x = torch.cat((states, actions), 1)
        x = self.fc3(self.activation(self.fc2(self.activation(self.fc1(x)))))
        return x

class Actor(nn.Module):

    def __init__(self,
                 observation_dims: int,
                 action_dims: int,
                 hidden_size: int,
                 activation: str):
        
        super(Actor, self).__init__()
        self.__observation_dims = observation_dims
        self.__action_dims = action_dims

        activation_layer = None
        if activation == 'relu':
            activation_layer = nn.ReLU()
        elif activation == 'tanh':
            activation_layer = nn.Tanh()
        else:
            raise NotImplementedError("Activation layer {} is not Supported yet.".format(activation))
        
        self.fc1 = nn.Linear(out_features=hidden_size, in_features=observation_dims)
        self.fc2 = nn.Linear(out_features=hidden_size, in_features=hidden_size)
        self.fc3 = nn.Linear(out_features=action_dims, in_features=hidden_size)
        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()
        self.activation = activation_layer
        self.init_weights(init_w=3e-3)
    
    def init_weights(self, init_w):
        self.fc1.weight.data = fanin_init(self.fc1.weight.data.size())
        self.fc2.weight.data = fanin_init(self.fc2.weight.data.size())
        self.fc3.weight.data.uniform_(-init_w, init_w)        
    
    @property
    def observation_dims(self):
        return self.__observation_dims

    @property
    def action_dims(self):
        return self.__action_dims
    
    def forward(self,
                states: torch.FloatTensor):
        x = states.view(-1, self.__observation_dims)
        x = self.fc3(self.activation(self.fc2(self.activation(self.fc1(x)))))
        return self.tanh(x)


if __name__ == "__main__":

    # Test data
    obs_dims = 256
    action_dims = 4
    hidden_size = 64
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Testing with {} device".format(device))

    random_obs = torch.rand(200, obs_dims).to(device)
    random_act = torch.rand(200, action_dims).to(device)
    

    # Test Critic
    critic = Critic(observation_dims=obs_dims,
                    action_dims=action_dims,
                    hidden_size=hidden_size,
                    activation='relu').to(device)

    out = critic(random_obs, random_act)
    

    # Test actor
    actor = Actor(observation_dims=obs_dims,
                  action_dims=action_dims,
                  hidden_size=hidden_size,
                  activation='tanh').to(device)
    out = actor(random_obs)

