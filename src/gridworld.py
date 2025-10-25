"""
gridworld.py

This file defines the Gridworld class, which encapsulates the
Markov Decision Process (MDP) for a 4x3 grid environment.
This is the classic "Russell-Norvig" environment.

Grid Layout (row, col):
(0,0) (0,1) (0,2) (0,3) [GOAL, +1]
(1,0) (1,1) [WALL] (1,2) (1,3) [TRAP, -1]
(2,0) [START] (2,1) (2,2) (2,3)

- States: 9 accessible states (squares)
- Actions: North, South, East, West
- Rewards:
    - +1 at (0,3)
    - -1 at (1,3)
    - -0.04 (living penalty) for all other states
- Transitions (Stochastic):
    - 0.8 chance of moving in the intended direction.
    - 0.1 chance of "slipping" 90 degrees left.
    - 0.1 chance of "slipping" 90 degrees right.
- Terminal States: (0,3) and (1,3)
"""
import collections

class Gridworld:
    def __init__(self):
        # Grid dimensions
        self.height = 3
        self.width = 4
        
        # State definitions
        self.start_state = (2, 0)
        self.wall_states = {(1, 1)}
        self.goal_state = (0, 3)
        self.trap_state = (1, 3)
        self.terminal_states = {self.goal_state, self.trap_state}
        
        # Rewards
        self.living_penalty = -0.04
        self.rewards = {
            self.goal_state: 1,
            self.trap_state: -1
        }
        
        # Actions and transitions
        self.actions = ['North', 'South', 'East', 'West']
        self.slip_prob = 0.1
        self.move_prob = 0.8
        
        # Build the list of all valid (non-wall) states
        self.states = set()
        for r in range(self.height):
            for c in range(self.width):
                if (r, c) not in self.wall_states:
                    self.states.add((r, c))

    def getStates(self):
        """Returns all valid states in the grid."""
        return self.states

    def getActions(self, state):
        """Returns valid actions for a given state."""
        if state in self.terminal_states:
            return []  # No actions can be taken from a terminal state
        return self.actions

    def getRewards(self, state):
        """Returns the reward for being in a state."""
        return self.rewards.get(state, self.living_penalty)

    def isTerminal(self, state):
        """Checks if a state is terminal."""
        return state in self.terminal_states

    def _check_move(self, state, move):
        """
        Helper function to check if a move is valid.
        If the move is invalid (off-grid or into a wall),
        it returns the *original* state.
        """
        next_r, next_c = state[0] + move[0], state[1] + move[1]
        next_state = (next_r, next_c)
        
        # Check for boundary or wall collision
        if (not (0 <= next_r < self.height) or
            not (0 <= next_c < self.width) or
            next_state in self.wall_states):
            return state  # Stay in the original state
        return next_state # Valid move

    def getTransitions(self, state, action):
        """
        Get the transition probabilities and next states for a given state-action.
        Returns a list of (probability, next_state) tuples.
        """
        if self.isTerminal(state):
            return []

        # Define the intended move and the "slip" moves
        moves = {
            'North': (-1, 0),
            'South': (1, 0),
            'East': (0, 1),
            'West': (0, -1)
        }
        
        slip_left = {
            'North': 'West',
            'South': 'East',
            'East': 'North',
            'West': 'South'
        }
        
        slip_right = {
            'North': 'East',
            'South': 'West',
            'East': 'South',
            'West': 'North'
        }
        
        intended_move = moves[action]
        left_move = moves[slip_left[action]]
        right_move = moves[slip_right[action]]
        
        # Calculate the resulting states for each possible outcome
        # Use a defaultdict to aggregate probabilities for the same next_state
        # (e.g., if intended move and slip move both hit a wall and stay)
        transitions = collections.defaultdict(float)
        
        # Intended move (80% chance)
        next_state_intended = self._check_move(state, intended_move)
        transitions[next_state_intended] += self.move_prob
        
        # Slip left (10% chance)
        next_state_left = self._check_move(state, left_move)
        transitions[next_state_left] += self.slip_prob
        
        # Slip right (10% chance)
        next_state_right = self._check_move(state, right_move)
        transitions[next_state_right] += self.slip_prob
        
        return list(transitions.items())
