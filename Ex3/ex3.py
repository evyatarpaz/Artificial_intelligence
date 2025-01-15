import zuma
import pickle

id = ["000000000"]


class Policy:
    """This class is a Policy for a Zuma game."""

    def __init__(self, game: zuma.Game):
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
        # tip to initialize table
        # arr = np.zeros((int(sum([math.pow(4, i) for i in range(max_line_length + 1)])), max_line_length+2))

        # generate policy here

    def choose_next_action(self, state):
        """Choose next action for Zuma given the current state of the game.
        state is a tuple of (line, ball_to_throw)
        """
        # use policy generated from init, Do not learn.
        return 0
        pass

    def save_policy(self, file):
        with open(file+'.pkl', 'wb') as f:
            pickle.dump(self, f)

    def load_policy(self, file):
        with open(file+'.pkl', 'rb') as f:
            obj = pickle.load(f)
        """
            assign every attribute of class from loaded object
            example
            self.max_steps = obj.max_steps
            self.initial_state = obj.initial_state
            self.game = obj.game
            self.table = obj.table
        """


