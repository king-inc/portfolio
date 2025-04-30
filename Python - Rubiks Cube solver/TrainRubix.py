from Classes.rubix_env import RubixEnv
from Classes.RubixDQN import *
from gymnasium.vector import AsyncVectorEnv
import numpy as np

if __name__ == "__main__":
    num_envs = 4
    env = RubixEnv()

    #envs = make_vec_env("RubixEnv-v0", num_envs=num_envs)
    envs = AsyncVectorEnv([lambda:env for _ in range(num_envs)])
    print("Hello World!")

    state_shape = (6,3,3)
    action_size = 12

    agent = DQNAgent(state_shape, action_size, num_envs)
    training = True
    if training:
        num_episodes = 2000
        target_update_interval = 10  # Frequency (in episodes) to update the target network
        max_steps_per_episode = 1000
        states = []
        for episode in range(num_episodes):
            # Reset the environment and get the initial state (replace this with your 3D state)
            states,infos = envs.reset()  # Assuming this returns a 3D state
            #print(np.shape(state))
            total_rewards = np.zeros(num_envs)
            
            for step in range(max_steps_per_episode):
                actions = agent.get_action(states)  # Choose an action using epsilon-greedy
                next_states, rewards, dones, _, _ = envs.step(actions)  # Take action in the environment
                total_rewards += rewards
                #print("work")
                # Store the experience in the replay buffer
                for i in range (num_envs):
                    agent.replay_buffer.add((states[i], actions[i], rewards[i], next_states[i], dones[i]))
                
                #print(f"Episode {episode + 1}/{num_episodes}, Reward: {reward}")
                states = next_states  # Move to the next state
                
                # Train the agent using experiences from the replay buffer
                agent.train()
                
                if np.any(dones):
                    print(f"Episode {episode + 1}/{num_episodes},Scatter Degree: {infos[0]}, Reward: {total_rewards}, DONE!")
                    break

            agent.Decay()
            print(f"Episode {episode + 1}/{num_episodes},Scatter Degree: {infos[0]}, Total Reward: {total_rewards}")
            # Update the target network every few episodes
            if episode % target_update_interval == 0:
                agent.update_target_network()
        
        agent.save("Agents/Rubix-v1.pth")

    else:
        agent.load("Agents/Rubix-v0")

        states, infos = envs.reset()
        done = False
        print(f"Scatter Degree: {infos}")
        total_rewards = np.zeros(num_envs)
        dones = []
        actions_taken = 0

        while not done:
            actions = agent.exploit(states)
            next_states, rewards, dones, _, _ = envs.step(actions)
            # Update the state and accumulate rewards
            states = next_states
            total_rewards += rewards
            actions_taken += 1
            print (f"Actions: {actions}, Rewards: {rewards}")

            if np.any(dones):
                break
        print(f"Scatter Degree: {infos[0]}, Actions Taken: {actions_taken}, Dones: {dones}")
