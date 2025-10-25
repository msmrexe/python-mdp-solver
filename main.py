"""
main.py

This is the main executable script for the MDP Gridworld Solver.
It uses argparse to parse command-line arguments and runs the
specified solver algorithm on the Gridworld.

Example Usage:
python main.py -a value_iteration
python main.py --algorithm policy_iteration
"""

import argparse
from src.gridworld import Gridworld
from src.solver import value_iteration, policy_iteration

def print_policy(policy, gridworld):
    """Prints the policy grid to the console."""
    action_symbols = {
        'North': '^',
        'South': 'v',
        'East':  '>',
        'West':  '<',
        None:    '.'
    }
    
    print("Optimal Policy:")
    for r in range(gridworld.height):
        row_str = ""
        for c in range(gridworld.width):
            state = (r, c)
            if state in gridworld.wall_states:
                row_str += "  #  "
            elif state == gridworld.goal_state:
                row_str += "  G  "
            elif state == gridworld.trap_state:
                row_str += "  T  "
            else:
                action = policy.get(state)
                symbol = action_symbols.get(action, '?')
                row_str += f"  {symbol}  "
        print(row_str)
        print()

def print_utilities(utilities, gridworld):
    """Prints the utility values for each state."""
    print("Optimal Utilities:")
    for r in range(gridworld.height):
        row_str = ""
        for c in range(gridworld.width):
            state = (r, c)
            if state in gridworld.wall_states:
                row_str += "    #    "
            else:
                utility = utilities.get(state, 0.0)
                row_str += f" {utility: 6.2f} "
        print(row_str)
        print()

def main():
    """
    Parses arguments, runs the selected algorithm, and prints the results.
    """
    parser = argparse.ArgumentParser(
        description="Solve a Gridworld MDP using Value or Policy Iteration."
    )
    
    parser.add_argument(
        '-a', '--algorithm', 
        type=str, 
        default='value_iteration', 
        choices=['value_iteration', 'policy_iteration'],
        help="The solver algorithm to use (default: value_iteration)"
    )
    
    args = parser.parse_args()
    
    # Initialize the environment
    gridworld = Gridworld()
    
    print(f"Running {args.algorithm}...")
    
    if args.algorithm == 'value_iteration':
        policy, utilities = value_iteration(gridworld)
    else:
        policy, utilities = policy_iteration(gridworld)
        
    print("-" * 30)
    print_utilities(utilities, gridworld)
    print("-" * 30)
    print_policy(policy, gridworld)
    print("-" * 30)

if __name__ == "__main__":
    main()
