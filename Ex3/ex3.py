import re
import zuma
import pickle
import numpy as np
import os

id = ["000000000"]


class Policy:
    """This class is a Policy for a Zuma game."""

    def __init__(self, game: zuma.Game,q_table_file='q_table50mr10_vector'):
        """Initialize and generate Policy for given game model.
        This method MUST terminate within the specified timeout.

        methods in game that you're able to use:
        new_line, new_ball, reward_for_action, is_done = game.submit_next_action(index/or -1)
        total_reward for_episode = game.play_game(policy)
        current_line, current_ball, current_step, max_steps = game.get_current_state()
        game.reset(generate_new_line=False)
        """
        self.game = game
        self.max_steps = game.get_current_state()[3]
        self.initial_state = game.get_current_state()[:2]
        self.max_line_length = game._max_length
        self.state_to_index_cache = {}
        num_states = int(sum([np.power(4, i) for i in range(self.max_line_length + 1)]) * 4)
        num_actions = self.max_line_length + 2

        # Initialize the Q-table with zeros
        # the number of states are 4^1 + 4^2 + 4^3 + ... + 4^max_line_length and the number of actions are max_line_length + 2
        self.q_table = np.zeros((num_states, num_actions))
        
        # check if the policy(q_table_vector) exists
        if os.path.exists((q_table_file + ".npz")):
            # if the q_table exists load it
            self.load_policy(q_table_file)
        else:
            # if the q_table does not exist train it
            self.load_cache("state_to_index_cache")
            self.train_q_table()
            self.save_policy(q_table_file)
                      
    def state_to_index(self, line, ball):
        """Convert a state to an index in the Q-table."""
        # if the index of the state is not in the cache calculate it and add it to the cache
        if (tuple(line), ball) not in self.state_to_index_cache:
            index = sum(color * (4 ** i) for i, color in enumerate(line))
            index = (index * 4) + (ball - 1) - 4
            self.state_to_index_cache[(tuple(line), ball)] = index
        return self.state_to_index_cache[(tuple(line), ball)]
                    
    def train_q_table(self):
        alpha = 0.15  # Initial learning rate
        
        gamma = 0.95  # Discount factor
        
        epsilon = 1  # Initial exploration rate
        
        num_episodes = 50 * (10**6)  # Total episodes 50 million
        
        epsilon_min = 0.01  # Minimum exploration rate
        
        # Decay rate for epsilon a function that i found that works well it decay the epsilon 
        # to the minimum value in the num_episodes
        epsilon_decay = np.exp(np.log(epsilon_min / epsilon) / num_episodes)
        
        # for me to see the progress of the training
        reward_f = 0
        reward_per_100000 = 0

        
        for episode in range(1,num_episodes + 1):
            
            # Reset the game and create a random state
            self.game.reset(True)
            
            # Get the current state of the game
            state = self.game.get_current_state()
            
            done = False
            total_reward = 0
            
            # while the game is not done(finshed or lost) do the following
            while not done:
                
                # Choose an action
                # get a rundom number between 0 and 1 if it is less than epsilon choose a random action
                # else choose the best action from the q_table
                action = (
                np.random.choice(range(-1, len(state[0]) + 1))
                if np.random.random() < epsilon
                else (np.argmax(self.q_table[self.state_to_index(state[0],state[1]), :]) - 1)
                )
                
                # get the line and ball of the current state
                state_line,ball,_,_ = state
                
                # get the index of the state in the q_table
                state_index = self.state_to_index(state_line,ball)
                
                # submit the action to the game and get the new state and the reward for the action
                new_line, new_ball, reward_for_action, done = self.game.submit_next_action(action)
                
                # if the reward is positive multiply it by 10 else keep it as it is.
                # I found that this works well for the training
                # it reanforces the agent to take the right actions
                # it reanforces the positive actions.
                reward = 0
                if reward_for_action > 0:
                    reward = reward_for_action * 10
                else:
                    reward = reward_for_action
                
                # get the index of the new state in the q_table
                next_state_index = self.state_to_index(new_line, new_ball)
                
                # get the old value of the q_table for the current state and action
                old_value = self.q_table[state_index, action + 1]
                
                # get the max value of the q_table for the new state
                next_max = np.max(self.q_table[next_state_index, :])
                
                # update the q_table with the new value by the formula
                self.q_table[state_index,action + 1] = (1-alpha)*old_value + alpha*(reward + gamma*next_max)
                
                # update the state to the new state
                state = self.game.get_current_state()
                
                # for me to see the progress of the training
                total_reward += reward_for_action    
                reward_f += total_reward
                reward_per_100000 += total_reward  
            
            # Decay the exploration rate    
            epsilon = max(epsilon_min, epsilon*epsilon_decay)
            
            # for me to see the progress of the training
            if episode % 10000 == 0:
                print(f"Episode: {episode}, Epsilon: {epsilon}, Total Reward: {total_reward}, last reward: {reward_for_action}, agv reward all: {reward_f/episode}, alpha: {alpha}, re100000: {reward_per_100000/10000}")
                reward_per_100000 = 0
        # for me to see the progress of the training
        print("agv Total Reward: ", reward_f/num_episodes)
        
        # done training reset the game with the initial state
        self.game.reset()
        
    def choose_next_action(self, state):
        """Choose next action for Zuma given the current state of the game.
        state is a tuple of (line, ball_to_throw)
        """
        # get the index of the state in the q_table
        state_index = self.state_to_index(state[0], state[1])
        
        # return the action in the q_table_vector(the vector have the index of the best action for each state)
        return int(self.q_table[state_index]) - 1

    # a function that saves the policy(q_table_vector) to a file npz
    def save_policy(self, file):
        with open(file+'.pkl', 'wb') as f:
            pickle.dump(self, f)
        np.savez_compressed(file, q_table=self.q_table)
        vector = np.zeros(self.q_table.shape[0])
        for i in range(self.q_table.shape[0]):
            vector[i] = np.argmax(self.q_table[i, :])
        np.savez_compressed(file + "_vector", q_table=vector)

    def load_policy(self, file):
        data = np.load(file + ".npz")
        self.q_table = data['q_table']

    # A fuction that help to load the cache of the index of the states
    # So the train will be faster nad more efficient
    # Only for training purposes
    def load_cache(self, file):
        with open(file+'.pkl', 'rb') as f:
            obj = pickle.load(f)
            # self.q_table = obj.q_table
            self.state_to_index_cache = obj.state_to_index_cache
