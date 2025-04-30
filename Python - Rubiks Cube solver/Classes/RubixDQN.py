import gymnasium
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque
import pickle

class DQNetwork(nn.Module):
    def __init__(self, state_shape, action_size):
        super(DQNetwork, self).__init__()
        
        # Convolutional layers
        self.conv1 = nn.Conv2d(in_channels=state_shape[0], out_channels=32, kernel_size=3, stride=1)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=1, stride=1)
         
        # Calculate the size of the flattened output after the conv layers
        conv_output_size = 64 * 1 * 1
        
        # Fully connected layers
        #print(conv_output_size)
        self.fc1 = nn.Linear(conv_output_size, 128)
        self.fc2 = nn.Linear(128, action_size)
    
    def forward(self, state):
        #print(state)
        x = torch.relu(self.conv1(state))
        x = torch.relu(self.conv2(x))
        x = x.view(x.size(0), -1)  # Flatten the convolutional output
        x = torch.relu(self.fc1(x))
        q_values = self.fc2(x)
        return q_values


class ReplayBuffer:
    def __init__(self, buffer_size, batch_size):
        self.buffer = deque(maxlen=buffer_size)
        self.batch_size = batch_size
    
    def add(self, experience):
        """Adds an experience (state, action, reward, next_state, done) to the buffer."""
        self.buffer.append(experience)
    
    def sample(self):
        """Samples a random batch of experiences from the buffer."""
        minibatch = random.sample(self.buffer, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*minibatch)
        
        # Convert the states and next states from list to tensor
        states = torch.FloatTensor(np.array(states))
        next_states = torch.FloatTensor(np.array(next_states))
        actions = torch.LongTensor(actions).unsqueeze(1)
        rewards = torch.FloatTensor(rewards)
        dones = torch.FloatTensor(dones)
        
        return states, actions, rewards, next_states, dones
    
    def size(self):
        return len(self.buffer)


class DQNAgent:
    def __init__(self, state_shape, action_size,num_envs):
        self.state_shape = state_shape
        self.action_size = action_size
        self.num_envs = num_envs
        
        # Hyperparameters
        self.gamma = 0.99        # Discount factor
        self.epsilon = 1.0       # Exploration rate
        self.epsilon_min = 0.01  # Minimum exploration rate
        self.epsilon_decay = 0.9987 #0.9987
        self.learning_rate = 0.001
        self.batch_size = 128
        self.buffer_size = 10000000
        
        # Q-Network and Target Network
        self.q_network = DQNetwork(state_shape, action_size)
        self.target_network = DQNetwork(state_shape, action_size)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=self.learning_rate)
        
        # Experience replay buffer
        self.replay_buffer = ReplayBuffer(self.buffer_size, self.batch_size)
        
        # Synchronize the target network with the Q-network
        self.update_target_network()
    
    def save(self, file_path):
        torch.save(self.q_network.state_dict(), file_path)
        #with open("replay_buffer.pkl","wb") as f:
            #pickle.dump(self.replay_buffer, f)

    def load(self, file_path):
        self.q_network.load_state_dict(torch.load(file_path))
    def update_target_network(self):
        """Synchronizes the target network with the Q-network."""
        self.target_network.load_state_dict(self.q_network.state_dict())
    
    def get_action(self, states):
        """Selects an action using the epsilon-greedy policy."""
        actions = []
        for state in states:
            if np.random.rand() <= self.epsilon:
                actions.append(random.randrange(0, self.action_size))  # Explore
            else:
                # Convert state to a tensor for the CNN (assumes (batch_size, channels, height, width))
                state_tensor = torch.FloatTensor(state).unsqueeze(0)  # Add batch dimension
                q_values = self.q_network(state_tensor)
                actions.append(torch.argmax(q_values).item())  # Exploit
        return actions
    
    def exploit(self, states):
        actions = []
        for state in states:
        # Convert state to a tensor for the CNN (assumes (batch_size, channels, height, width))
            state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)  # Add batch dimension
            with torch.no_grad():
                q_values = self.q_network(state_tensor)  # Predict Q-values for the current state
            actions.append(torch.argmax(q_values).item())  # Exploit
        return actions
    
    def train(self):
        """Trains the Q-network by sampling experiences from the replay buffer."""
        if self.replay_buffer.size() < self.batch_size*10:
            return  # Not enough experiences to sample
        
        # Sample a batch of experiences from the replay buffer
        states, actions, rewards, next_states, dones = self.replay_buffer.sample()
        
        # Get the predicted Q-values for the current state-action pairs
        q_values = self.q_network(states).gather(1, actions)
        
        # Get the maximum Q-value for the next state from the target network
        next_q_values = self.target_network(next_states).max(1)[0].detach()
        
        # Compute the target Q-values
        target_q_values = rewards + (self.gamma * next_q_values * (1 - dones))
        
        # Compute loss (MSE between predicted Q-values and target Q-values)
        loss = nn.MSELoss()(q_values.squeeze(), target_q_values)
        
        # Perform a gradient descent step to minimize the loss
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        

    def Decay(self):
        # Update epsilon (exploration rate)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
