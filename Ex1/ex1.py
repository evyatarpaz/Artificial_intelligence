import re

import search
import utils

ids = ["No numbers - I'm special!"]

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
        utils.raiseNotDefined()

    def goal_test(self, state):
        """ given a state, checks if this is the goal state, compares to the created goal state"""
        utils.raiseNotDefined()

    def h(self, node):
        """ This is the heuristic. It gets a node (not a state)
        and returns a goal distance estimate"""
        utils.raiseNotDefined()


def create_zuma_problem(game):
    print("<<create_zuma_problem")
    """ Create a zuma problem, based on the description.
    game - pair of lists as described in pdf file"""
    return ZumaProblem(game)


# game = ()

# create_zuma_problem(game)
