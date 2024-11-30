import re
import ex1_check
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
        stateLine, stateAmmo = state

        ball_in_line = {}
        ball_in_ammo = {}

        # Count the color in the line
        for ball in stateLine:
            if ball not in ball_in_line:
                ball_in_line[ball] = 0
            ball_in_line[ball] += 1

        # Count the color in the ammo
        for ball in stateAmmo:
            if ball not in ball_in_ammo:
                ball_in_ammo[ball] = 0
            ball_in_ammo[ball] += 1

        
        for ball in COLORS:
            # If the ball is in both the line and the ammo
            if ball in ball_in_ammo and ball in ball_in_line:
                # If the ball is in the line and the ammo and the combined count is less than 3
                if ball_in_ammo[ball] + ball_in_line[ball] < 3:
                    return succ  # No solution if combined count is less than 3
                continue
            # If the ball is not in the ammo and  in the line
            elif ball not in ball_in_ammo and ball in ball_in_line:
                if ball_in_line[ball] < 3:
                    return succ  # No solution if line count is less than 3
                continue
            
            
        seen = set()
        potential = set()
        ball = stateAmmo[0]
        newAmmo = stateAmmo[1:]

        # a single check if the ball is in the ammo and not in the line and the count is less than 3
        if ball in ball_in_ammo and ball not in ball_in_line and ball_in_ammo[ball] < 3:
            succ.append((-1, (stateLine, newAmmo)))  # its gernteed that the ball will be skipped
            return succ
        
        for i in range(len(stateLine)):
            if i < len(stateLine) - 1 and stateLine[i] == stateLine[i + 1]:
                if ball == stateLine[i]:
                    potential.add(i + 1)
                else:
                    potential.add(i + 1)
                    potential.add(i + 2)
                    potential.add(i)
            if ball == stateLine[i]:
                potential.add(i + 1)

        for var in potential:
            new_line = stateLine[:var] + (ball,) + stateLine[var:]
            new_line = self.remove_three_balls(new_line)
            if ((new_line, newAmmo)) in seen:
                continue
            seen.add((new_line, newAmmo))
            succ.append((var, (new_line, newAmmo)))  

        # Add the skip option    
        succ.append((-1, (stateLine, newAmmo)))

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
        return 1

def create_zuma_problem(game):
    print("<<create_zuma_problem")
    """ Create a zuma problem, based on the description.
    game - pair of lists as described in pdf file"""
    return ZumaProblem(game)

if __name__ == '__main__':
    ex1_check.main()