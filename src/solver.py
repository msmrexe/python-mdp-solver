"""
solver.py

This file implements the two core algorithms for solving MDPs:
- Value Iteration
- Policy Iteration
"""
import random

def value_iteration(gridworld, discount=0.9, max_iterations=100, epsilon=1e-4):
    """
    Performs Value Iteration to find the optimal utility function and policy.
    
    Returns:
        policy (dict): A dictionary {state: action}
        U (dict): A dictionary {state: utility}
    """
    states = gridworld.getStates()
    U = {state: 0.0 for state in states}

    for _ in range(max_iterations):
        U_new = U.copy()
        delta = 0
        
        for state in states:
            if gridworld.isTerminal(state):
                U_new[state] = gridworld.getRewards(state)
                continue
            
            # Calculate Q-value for each action
            action_values = []
            for action in gridworld.getActions(state):
                q_value = 0
                for prob, next_state in gridworld.getTransitions(state, action):
                    q_value += prob * U[next_state]
                action_values.append(q_value)
            
            # Bellman update
            best_q = max(action_values) if action_values else 0
            U_new[state] = gridworld.getRewards(state) + discount * best_q
            
            # Check for convergence
            delta = max(delta, abs(U_new[state] - U[state]))
            
        U = U_new
        if delta < epsilon * (1 - discount) / discount:
            break
            
    # After convergence, extract the optimal policy
    policy = {}
    for state in states:
        if gridworld.isTerminal(state):
            policy[state] = None
            continue
            
        best_action = None
        best_q = -float('inf')
        
        for action in gridworld.getActions(state):
            q_value = 0
            for prob, next_state in gridworld.getTransitions(state, action):
                q_value += prob * U[next_state]
                
            if q_value > best_q:
                best_q = q_value
                best_action = action
        policy[state] = best_action
        
    return policy, U

def policy_iteration(gridworld, discount=0.9, max_iterations=100, epsilon=1e-4):
    """
    Performs Policy Iteration to find the optimal policy.
    
    Returns:
        policy (dict): A dictionary {state: action}
        U (dict): A dictionary {state: utility}
    """
    states = gridworld.getStates()
    
    # 1. Initialize a random policy
    policy = {}
    for state in states:
        if gridworld.isTerminal(state):
            policy[state] = None
        else:
            policy[state] = random.choice(gridworld.getActions(state))
            
    U = {state: 0.0 for state in states}
    
    for _ in range(max_iterations):
        policy_stable = True
        
        # 2. Policy Evaluation: Calculate utilities for the current policy
        # We run a simplified version of value iteration
        for _ in range(max_iterations):
            U_new = U.copy()
            delta = 0
            for state in states:
                if gridworld.isTerminal(state):
                    U_new[state] = gridworld.getRewards(state)
                    continue

                action = policy[state]
                q_value = 0
                for prob, next_state in gridworld.getTransitions(state, action):
                    q_value += prob * U[next_state]
                
                U_new[state] = gridworld.getRewards(state) + discount * q_value
                delta = max(delta, abs(U_new[state] - U[state]))
                
            U = U_new
            if delta < epsilon * (1 - discount) / discount:
                break
        
        # 3. Policy Improvement: Find a new, better policy
        for state in states:
            if gridworld.isTerminal(state):
                continue
                
            old_action = policy[state]
            
            best_action = None
            best_q = -float('inf')
            
            for action in gridworld.getActions(state):
                q_value = 0
                for prob, next_state in gridworld.getTransitions(state, action):
                    q_value += prob * U[next_state]
                
                if q_value > best_q:
                    best_q = q_value
                    best_action = action
            
            policy[state] = best_action
            
            if old_action != best_action:
                policy_stable = False
                
        # If the policy did not change, we have converged
        if policy_stable:
            break
            
    return policy, U
