import zuma
import ex3
import time
import pandas as pd

# The example model configuration
example = {
    'chosen_action_prob': {1: 0.6, 2: 0.7, 3: 0.5, 4: 0.9},
    'next_color_dist': {1: 0.1, 2: 0.6, 3: 0.15, 4: 0.15},
    'color_pop_prob': {1: 0.6, 2: 0.7, 3: 0.4, 4: 0.9},
    'color_pop_reward': {'3_pop': {1: 3, 2: 1, 3: 2, 4: 2},
                         'extra_pop': {1: 1, 2: 2, 3: 3, 4: 1}},
    'color_not_finished_punishment': {1: 2, 2: 3, 3: 5, 4: 1},
    'finished_reward': 150,
    'seed': 42
}

# Define the list of problems
problems = [
    (5, 2, [1, 4]),
    (5, 4, [4, 4]),
    (5, 6, [1, 4, 3, 3]),
    (5, 8, [3, 2, 3, 3]),
    (5, 10, [1, 1, 2, 4, 4, 4, 1, 3]),
    (10, 2, [1, 4]),
    (10, 4, [4, 4]),
    (10, 6, [1, 4, 2]),
    (10, 8, [3, 2, 3, 3]),
    (10, 10, [1, 1, 2, 4, 4, 4, 1, 3]),
    (20, 2, [1, 4]),
    (20, 4, [4, 4]),
    (20, 6, [1, 4, 2]),
    (20, 8, [3, 2, 3, 3]),
    (20, 10, [1, 1, 2, 4, 4, 4, 1, 3]),
    (30, 2, [1, 4]),
    (30, 4, [4, 4]),
    (30, 6, [1, 4, 2]),
    (30, 8, [3, 2, 3, 3]),
    (30, 10, [1, 1, 2, 4, 4, 4, 1, 3]),
    (40, 2, [1, 4]),
    (40, 4, [4, 4]),
    (40, 6, [1, 4, 2]),
    (40, 8, [3, 2, 3, 3]),
    (40, 10, [1, 1, 2, 4, 4, 4, 1, 3]),
    (50, 2, [1, 4]),
    (50, 4, [4, 4]),
    (50, 6, [1, 4, 2]),
    (50, 8, [3, 2, 3, 3]),
    (50, 10, [1, 1, 2, 4, 4, 4, 1, 3]),
]

def run_test(problems, debug=False):
    """Run the test for each problem using multiple seeds and generate a results table."""
    results = []  # To store results for the table
    
    for problem in problems:
        max_steps, max_length, initial_line = problem
        print(f"Test #{problem}...")
        
        scores = []
        
            
        # Create a new game instance
        game = zuma.create_zuma_game((max_steps, max_length, initial_line, example, debug))
            
            # Solve the problem
        policy = ex3.Policy(game)
        t2 = time.time()
        avg_score = game.evaluate_policy(policy, 5000, visualize=False)
        t3 = time.time()
            
            # Collect results
        scores.append(avg_score)
        print(f"Average Score = {avg_score:.2f}, Eval Time: {t3 - t2:.2f}s")
        
        # Compute aggregate metrics for the problem
        avg_score = sum(scores) / len(scores)

        results.append({"Turns": max_steps ,"Max length": max_length,"Avg Score": avg_score})
        
        # Print overall results for the problem
        print(f"Average Score = {avg_score:.2f}")
        print("=" * 50)
    
    # Generate and display the results table
    results_df = pd.DataFrame(results)
    print("\nTest Results Summary:")
    print(results_df)
    return results_df

if __name__ == "__main__":
    results_table = run_test(problems, debug=False)
