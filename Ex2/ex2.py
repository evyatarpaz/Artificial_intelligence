import zuma
import copy
import random
import re
id = ["211788625"]

class Controller:
    """This class is a controller for a Zuma game."""

    def __init__(self, game: zuma.Game):
        """Initialize controller for given game model.
        This method MUST terminate within the specified timeout.
        """
        self.original_game = game
        self.copy_game = copy.deepcopy(game)
    
    def potential_actions(self, line, current_ball) -> set:
        """Return the potential actions for the game.
        """
        potential = set()
        length = len(line)
        for i in range(length):
            # Add position after the current ball
            if current_ball == line[i]:
                potential.add(i + 1)  
        # Add the action to not insert the ball
        potential.add(-1)
        # Add the action to insert at the beginning if no other actions
        if len(potential) == 1:
            potential.add(0)
        return potential

    def all_states(self, line, length, current_ball) -> list:
        """Return all states of the game.
        """
        all_states = []
        for i in range(length + 1):
            # Insert ball at every possible position
            new_line = line[:i] + [current_ball] + line[i:]
            all_states.append(new_line)
        # Add the original line as a state
        all_states.append(line)  
        return all_states
    
    def _remove_group(self, line, addition, reward=0):
        """
        Removes groups of balls according to their pop probability.
        :param line: list (sequence of balls to check for pops)
        :param addition: int (index of ball insertion)
        :param reward: int (reward of current insertion)
        :return: tuple (updated sequence of balls as list, reward of insertion as int, updated addition index as int, flag indicating if further removal is needed as bool, ball type as int)
        """
        burstable = re.finditer(r'1{3,}|2{3,}|3{3,}|4{3,}', ''.join([str(i) for i in line]))
        new_reward = reward
        new_line = line.copy()
        ball = 0
        for group in burstable:
            if addition in range(group.span()[0], group.span()[1]):
                new_reward += (self.original_game._color_pop_reward['3_pop'][line[group.start()]] 
                               + (group.span()[1] - group.span()[0] - 3) *
                                self.original_game._color_pop_reward['extra_pop'][line[group.start()]])
                new_line = line[:group.span()[0]] + line[group.span()[1]:]
                ball = line[group.start()]
                addition = group.span()[0]
            break
        if not new_line:
            # Add empty line reward if the line is empty
            reward += self.original_game._finished_reward
            
            # if the line is empty return false there is no need to remove more balls
            return new_line, new_reward, addition, False, ball
        
        # if the new line is different from the old line, return true to continue removing balls
        if new_line != line:
            return new_line, new_reward, addition, True, ball 
        # if the new line is the same as the old line, return false there is no need to remove more balls
        return new_line, new_reward, addition, False, ball
    
    
    def calculate_expected_reward(self, action, current_ball, new_line, action_flag):
        expected_reward = 0
        flag = True
        new_reward = 0
        rewards = []
        balls = []
        pop_prob = []
        # if the remove_groupe function returns true, continue removing balls
        while flag:
            new_line, new_reward, action, flag, ball = self._remove_group(new_line, action, new_reward)
            # if the ball is not 0, that means a group of balls has been removed
            if ball != 0:
                # save the reward of the group that has been removed
                rewards.append(new_reward)
                # save the type of ball that has been removed
                balls.append(ball)
        prob = 1
        # calculate all posible probabilities of the balls that have been removed
        # exmple:prob[3] = pop(0) * pop(1) * pop(2) * pop(3)]
        for i in range(len(balls)):
            prob = prob * self.original_game._color_pop_prob[balls[i]]
            pop_prob.append(prob)  
            
        # calculate the expected reward of the balls that have been removed     
        chosen_action_prob = self.original_game._chosen_action_prob[current_ball]
        for i in range(len(rewards)):
            # if i succ in inserting the ball
            if action_flag:
                if i > 1:
                    # if there where more then 1 balls removed
                    # calculate the expected reward by the formula
                    # p(success) * p(0) * reward(0) + p(success) * p(0) * p(1) * reward(1) + p(success) * p(0) * (1-p(1)) * reward(1) ......
                    expected_reward += chosen_action_prob * pop_prob[i] * rewards[i]
                    + chosen_action_prob * (1 - self.original_game._color_pop_prob[balls[i]]) * pop_prob[i-1] * rewards[i]
                else:
                    expected_reward += chosen_action_prob * pop_prob[i] * rewards[i]
            else:
                if i > 1:
                    # p(not-succ) * p(0) * reward(0) + p(not-succ) * p(0) * p(1) * reward(1) + p(not-succ) * p(0) * (1-p(1)) * reward(1) ......
                    expected_reward += (1 - chosen_action_prob) * pop_prob[i] * rewards[i]
                    + (1 - chosen_action_prob) * (1 - self.original_game._color_pop_prob[balls[i]]) * pop_prob[i-1] * rewards[i] 
                else:
                    expected_reward += (1 - chosen_action_prob) * pop_prob[i] * rewards[i]
                    
        return expected_reward
    
    def choose_next_action(self):
        """Choose next action for Zuma given the current state of the game.
        """
        
        max_rewards = - float('inf')
        line, current_ball, steps, max_steps = self.original_game.get_current_state()
        length = len(line)
        if length == 0:
            if self.original_game._chosen_action_prob[current_ball] >= (1 - self.original_game._chosen_action_prob[current_ball]):
                return -1  # No action needed if the line is empty
            else:
                return 0
        # get all the possible states of the game
        all_states = self.all_states(line, length, current_ball)    
        rewards_action = 0
        # default action
        chosen_action = -1
        # get all the potential actions
        actions = self.potential_actions(line, current_ball)
        # for every action
        for action in actions:
            # for every state that the action can lead to
            for i in range(-1, length + 1):
                # if the action succ
                if i == action:
                    # call the function with the flag true and calculate the expected reward
                    rewards_action += self.calculate_expected_reward(i, current_ball, all_states[i], True)
                else:
                    # call the function with the flag false and calculate the expected reward
                    rewards_action += self.calculate_expected_reward(i, current_ball, all_states[i], False)
                    
            # choose the action that has the maximum expected reward
            if rewards_action > max_rewards:
                max_rewards = rewards_action
                chosen_action = action
            rewards_action = 0
        return chosen_action
