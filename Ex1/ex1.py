import re

import search
import utils

ids = ["211788625"]

""" Rules """
RED = 1
BLUE = 2
YELLOW = 3
GREEN = 4
COLORS = [RED, BLUE, YELLOW, GREEN]


class ZumaProblem(search.Problem):
    """This class implements a pacman problem"""

    def __init__(self, initial):
        """ Magic numbers for balls:
        1 - red, 2 - blue, 3 - yellow, 4 - green."""

        self.line = initial[0]
        self.ammo = initial[1]

        """ Constructor only needs the initial state.
        Don't forget to set the goal or implement the goal test"""
        search.Problem.__init__(self, initial)

    def successor(self, state):
        """ Generates the successor state """
        succ = []

        # state = (line, ammo)
        stateLine, stateAmmo = state

        # if no ammo, return an empty successor list
        if not stateAmmo:
            return succ
        
        # get the first ball from the ammo
        ball = stateAmmo[0]

        # try to insert the ball in all possible places
        for i in range(len(stateLine) + 1):
            newLine = stateLine[:i] + (ball,) + stateLine[i:]
            newAmmo = stateAmmo[1:]
            newLine = self.remove_three_balls(newLine)
            succ.append((f"Insert {ball} at {i}", (newLine, newAmmo)))
        
        # try to skip the ball
        newAmmo = stateAmmo[1:]
        succ.append((f"Skip {ball}", (stateLine, newAmmo)))
        return succ
    
    # An helper function to remove 3 balls in a row
    def remove_three_balls(self, line):
        while True:
            found = False
            i = 0
            while i < len(line):
                j = i
                while j < len(line) and line[j] == line[i]:
                    j += 1
                if j - i >= 3:
                    line = line[:i] + line[j:]
                    found = True
                    break
                i = j
            if not found:
                break
        return line
    
    def goal_test(self, state):
        """ given a state, checks if this is the goal state, compares to the created goal state"""
        stateLine, stateAmmo = state

        # the only goal is an empty line otherwise there is no solution
        if not stateLine:
            return True
        return False



    def h(self, node):
        """ This is the heuristic. It gets a node (not a state)
        and returns a goal distance estimate"""
        line, ammo = node.state
        
        if not line:
            return 0
        
        heuristic = len(line) * 3

        for i in range(len(line) - 1):
            if line[i] == line[i + 1]:
                heuristic -= 2
        
        for ball in ammo:
            if ball in line:
                heuristic -= 1
        skip_count = 0
        for ball in ammo:
            if ball not in line:
                skip_count += 1
            else:
                break
        heuristic -= skip_count
        return heuristic


def create_zuma_problem(game):
    print("<<create_zuma_problem")
    """ Create a zuma problem, based on the description.
    game - pair of lists as described in pdf file"""
    return ZumaProblem(game)


# game = ((1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1), (1, 2, 3, 4, 1, 2, 3, 4))


# create_zuma_problem(game)