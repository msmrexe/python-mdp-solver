# MDP Gridworld Solver (Python)

This project provides a Python implementation of **Value Iteration** and **Policy Iteration** to solve a stochastic, grid-based Markov Decision Process (MDP). The environment is the classic 4x3 "Russell-Norvig" gridworld, which includes terminal states (a goal and a trap), walls, and stochastic transitions. The project was implemented for an Artificial Intelligence course.

## Features

* **Stochastic Environment:** The agent's actions are non-deterministic (80% chance of intended move, 10% slip left, 10% slip right).
* **Configurable MDP:** The `Gridworld` class cleanly defines states, actions, transitions ( $T(s, a, s')$ ), and rewards ( $R(s)$ ).
* **Value Iteration:** Implements the value iteration algorithm to find the optimal utility function.
* **Policy Iteration:** Implements the policy iteration algorithm, which alternates between policy evaluation and policy improvement.
* **Clear Visualization:** The `main.py` script prints the final utilities for each state and the optimal policy as a grid of arrows.

## AI & CS Concepts Showcased

* **Markov Decision Processes (MDPs):** The formal definition of the problem (States, Actions, Transitions, Rewards).
* **Dynamic Programming:** Both algorithms use dynamic programming to break the problem into smaller subproblems.
* **Bellman Equations:** The theoretical foundation for both algorithms.
* **Utility Functions:** Calculating the long-term "desirability" of a state ( $U(s)$ ).
* **Optimal Policies:** Determining the best action $\pi^*(s)$ to take in any given state.
* **Convergence:** Iterating until the utility functions or policy stabilize.

---

## How It Works

The system is built on two primary components: the environment (`gridworld.py`) and the solver (`solver.py`).

### 1. The Environment (`src/gridworld.py`)

The `Gridworld` class defines the entire MDP:
* **Grid:** A 4x3 world with a start state `(2,0)`, a wall at `(1,1)`, a goal at `(0,3)` (reward +1), and a trap at `(1,3)` (reward -1).
* **States:** All `(row, col)` tuples except the wall. The goal and trap are **terminal states**.
* **Rewards:** $R(s) = +1$ for the goal, $R(s) = -1$ for the trap, and $R(s) = -0.04$ (a "living penalty") for all other states to encourage efficiency.
* **Transitions ( $T(s, a, s')$ ):** The core of the MDP. `getTransitions(state, action)` returns a list of `(probability, next_state)` tuples. For any action, there is:
    * An 80% chance of moving in the intended direction.
    * A 10% chance of slipping 90 degrees to the "left" of the intended direction.
    * A 10% chance of slipping 90 degrees to the "right".
    * If any move would hit a wall or the boundary, the agent stays in its current state.

### 2. The Solvers (`src/solver.py`)

This file implements the two algorithms to solve the MDP defined by the `Gridworld`. Both use a `discount` factor $\gamma$ (gamma, default 0.9) to value immediate rewards over future rewards.

#### Value Iteration

**Goal:** To find the optimal utility function $U(s)$ by iteratively applying the Bellman update.

The algorithm starts with $U_0(s) = 0$ for all states. It then iterates, calculating $U_{i+1}(s)$ from the utilities of the previous iteration, $U_i(s)$.

The core of the algorithm is the **Bellman Update**:
$$U_{i+1}(s) \leftarrow R(s) + \gamma \max_{a} \sum_{s'} T(s, a, s') U_i(s')$$

* $R(s)$ is the reward for being in state $s$.
* $\gamma$ is the discount factor.
* $\max_{a}$ finds the best action $a$ by...
* ...calculating the expected utility of taking that action: $\sum_{s'} T(s, a, s') U_i(s')$. This sums the utility of each possible next state $s'$ weighted by its transition probability $T(s, a, s')$.

The algorithm stops when the utility function converges (i.e., the maximum change, $\delta$, is less than a small `epsilon`).

Finally, the **optimal policy $\pi^*(s)$** is extracted by choosing the action that maximizes the expected utility, using the final $U(s)$:
$$\pi^*(s) = \arg\max_{a} \sum_{s'} T(s, a, s') U(s')$$

#### Policy Iteration

**Goal:** To find the optimal policy $\pi(s)$ by alternating between two steps.

The algorithm starts with a random policy $\pi_0$.

1.  **Policy Evaluation:** Given the current policy $\pi_i$, calculate the utility function $U_i = U^{\pi_i}$ for that policy. This is done by solving a simplified version of the Bellman equation, where the $\max_{a}$ is replaced by the action $\pi_i(s)$ specified by the policy:
    $$U_i(s) = R(s) + \gamma \sum_{s'} T(s, \pi_i(s), s') U_i(s')$$
    This step is itself an iterative process (similar to Value Iteration) that is run until $U_i$ converges.

2.  **Policy Improvement:** Using the new utilities $U_i$, find a better policy $\pi_{i+1}$ by picking the best action for each state, just as in the final step of Value Iteration:
    $$\pi_{i+1}(s) = \arg\max_{a} \sum_{s'} T(s, a, s') U_i(s')$$

These two steps are repeated until the policy becomes **stable** (i.e., $\pi_{i+1} = \pi_i$).

### 3. The Main Executable (`main.py`)

This script ties everything together. It uses `argparse` to let you choose which algorithm to run, creates the `Gridworld`, calls the selected solver, and then uses helper functions to print a clean visualization of the final utilities and the optimal policy.

---

## Project Structure

```
python-mdp-solver/
├── .gitignore
├── LICENSE
├── README.md
├── main.py            # Main runnable script
└── src/
    ├── __init__.py    # Makes 'src' a package
    ├── gridworld.py   # Defines the MDP environment
    └── solver.py      # Value Iteration & Policy Iteration
```

## How to Use

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/msmrexe/python-mdp-solver.git
    cd python-mdp-solver
    ```

2.  **Run an Algorithm:**
    The `main.py` script is used to run the searches. The basic syntax is:
    `python main.py --algorithm <algorithm_name>`

    **Example (Value Iteration):**
    ```bash
    python main.py -a value_iteration
    ```

    **Example (Policy Iteration):**
    ```bash
    python main.py -a policy_iteration
    ```

    **Example Output:**
    ```
    Running value_iteration...
    ------------------------------
    Optimal Utilities:
     0.87   0.92   0.98    1.00 

     0.80     #     0.70   -1.00 

     0.74   0.68   0.63    0.55 

    ------------------------------
    Optimal Policy:
      >      >      >      G   

      ^      #      ^      T   

      ^      <      <      <   

    ------------------------------
    ```

---

## Author

Feel free to connect or reach out if you have any questions!

* **Maryam Rezaee**
* **GitHub:** [@msmrexe](https://github.com/msmrexe)
* **Email:** [ms.maryamrezaee@gmail.com](mailto:ms.maryamrezaee@gmail.com)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.
