import gymnasium as gym
from gymnasium import spaces
import numpy as np
from Classes.HelperFunctions import *
from gym.envs.registration import register


class RubixEnv(gym.Env):
    def __init__(self):
        super(RubixEnv, self).__init__()

        self.cube_size = 1

        self.action_space = spaces.Discrete(12)

        self.observation_space = spaces.Box(low=0,high=5,shape=(6,3,3),dtype=np.int32)

        self.start_cube = ScatterCube(CreateCube(),10)
        self.goal_cube = CreateCube()

        self.current_cube = self.start_cube
        self.current_state = self.current_cube.GetMatrixFaces()
        
    def reset(self,seed, options):
        degree = random.randint(0,10)
        self.current_cube = ScatterCube(CreateCube(),degree)
        #print("Scatter: ",degree)
        self.current_state = self.current_cube.GetMatrixFaces()
        return self.current_state, {0:degree}
    
    def step(self, action):
        self.current_cube = PerformAction(self.current_cube,action)
        self.current_state = self.current_cube.GetMatrixFaces()

        if self.current_cube == self.goal_cube:
            reward = 100
            done = True
        else:
            reward = CalculateReward(self.current_cube, self.goal_cube)
            done = False
        

        return self.current_state, reward, done, False, {}
    



        