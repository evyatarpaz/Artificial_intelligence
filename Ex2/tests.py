import zuma
import ex2
from copy import deepcopy

def solve(game: zuma.Game):
    policy = ex2.Controller(game)
    for _ in range(game.get_current_state()[3]):
        game.submit_next_action(chosen_action=policy.choose_next_action())
    return game.get_current_reward()

debug_mode = True

example = {
    'chosen_action_prob': {1: 0.6, 2: 0.7, 3: 0.5, 4: 0.9},
    'next_color_dist': {1: 0.1, 2: 0.6, 3: 0.15, 4: 0.15},
    'color_pop_prob': {1: 0.6, 2: 0.7, 3: 0.4, 4: 0.9},
    'color_pop_reward': {'3_pop': {1: 3, 2: 1, 3: 2, 4: 2},
                         'extra_pop': {1: 1, 2: 2, 3: 3, 4: 1}},
    'color_not_finished_punishment': {1: 2, 2: 3, 3: 5, 4: 1},
    'finished_reward': 150}

def main():
    
    num_seeds = 43
    seeds = range(num_seeds)

    # Define games
    games = [
        (200, [1, 1], example, debug_mode),
        (200, [1, 2, 3, 3, 3, 4, 2, 1, 2, 3, 4, 4], example, debug_mode),
        (200, [1, 2, 3, 3, 3, 4, 2, 1, 2, 3, 4, 4], example, debug_mode),
        (200, [1, 2, 1, 2, 1, 2, 1, 2], example, debug_mode),
        (200, [3, 3, 3, 3, 3, 4, 4, 4, 4, 4], example, debug_mode),
        (200, [1, 4, 2, 3, 4, 1, 3, 2, 4, 1], example, debug_mode),
        (200, [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3], example, debug_mode),
        (200, [1, 4, 4, 2, 2, 3, 3, 1, 1, 4, 4, 2, 2, 3, 3], example, debug_mode),
        (200, [1, 2, 1, 2, 3], example, debug_mode),
        (200, [4, 3, 4, 3, 4], example, debug_mode),
        (200, [2, 2, 3, 3, 4], example, debug_mode),
        (200, [1, 1, 1, 2, 2], example, debug_mode),
        (200, [4, 1, 4, 1, 3], example, debug_mode),
        (200, [1, 4, 1, 4, 2], example, debug_mode),
        (200, [2, 3, 2, 3, 4], example, debug_mode),
        (200, [3, 3, 2, 2, 1], example, debug_mode),
        (200, [1, 2, 3, 1, 2], example, debug_mode),
        (200, [4, 4, 4, 3, 2], example, debug_mode),
        (200, [3, 4, 2, 4, 3], example, debug_mode),
        (200, [1, 2, 4, 1, 3], example, debug_mode),
        (200, [2, 2, 1, 3, 1], example, debug_mode),
        (200, [3, 1, 3, 4, 2], example, debug_mode),
        (200, [4, 1, 2, 4, 3], example, debug_mode)   
    ]
    results= []  # Store average rewards for each gam200
    for idx, game_config in enumerate(games, start=1):
        cumulative_reward = 0

        for seed in seeds:
            # Deepcopy to ensure the configuration is reset for each seed
            game_config_copy = deepcopy(game_config)

            # Set the seed in the game configuration
            game_config_copy[2]['seed'] = seed

            # Create a new game instance
            game = zuma.create_zuma_game(game_config_copy)
            
            # Solve the game and accumulate the reward
            cumulative_reward += solve(game)

        # Compute the average reward and store it
        avg_reward = cumulative_reward / num_seeds
        results.append(avg_reward)
        print(f'Game {idx} -> Avg Reward: {avg_reward}\n')

    # Write results to the file
    with open("results", "w") as result_file:
        for idx, avg_reward in enumerate(results, start=1):
            result_file.write(f"{idx}. {avg_reward}\n")


    print("Results written to file 'results'.\n")

if __name__ == "__main__":
    main()
