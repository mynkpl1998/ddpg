import torch
import torch.nn as nn

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

        # Create a 3-layered fully connected critic network
        self.critic = nn.Sequential(
            nn.Linear(out_features=hidden_size, in_features=observation_dims + action_dims),
            activation_layer,
            nn.Linear(out_features=hidden_size, in_features=hidden_size),
            activation_layer,
            nn.Linear(out_features=hidden_size, in_features=hidden_size),
            activation_layer,
            nn.Linear(out_features=1, in_features=hidden_size)
        )

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
        x = x.view(-1, self.observation_dims + self.action_dims)
        return self.critic(x)

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
        
        # Create a 3-layered fully connected actor network
        self.actor = nn.Sequential(
            nn.Linear(out_features=hidden_size, in_features=observation_dims),
            activation_layer,
            nn.Linear(out_features=hidden_size, in_features=hidden_size),
            activation_layer,
            nn.Linear(out_features=hidden_size, in_features=hidden_size),
            activation_layer,
            nn.Linear(out_features=action_dims, in_features=hidden_size)
        )

    @property
    def observation_dims(self):
        return self.__observation_dims

    @property
    def action_dims(self):
        return self.__action_dims
    
    def forward(self,
                states: torch.FloatTensor):
        states = states.view(-1, self.__observation_dims)
        return self.actor(states)


if __name__ == "__main__":

    # Test data
    obs_dims = 256
    action_dims = 4
    hidden_size = 64
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Testing with {} device".format(device))

    random_obs = torch.rand(2, obs_dims).to(device)
    random_act = torch.rand(2, action_dims).to(device)
    
    # Test Critic
    critic = Critic(observation_dims=obs_dims,
                    action_dims=action_dims,
                    hidden_size=hidden_size,
                    activation='tanh').to(device)

    out = critic(random_obs, random_act)
    

    # Test actor
    actor = Actor(observation_dims=obs_dims,
                  action_dims=action_dims,
                  hidden_size=hidden_size,
                  activation='tanh').to(device)
    out = actor(random_obs)
