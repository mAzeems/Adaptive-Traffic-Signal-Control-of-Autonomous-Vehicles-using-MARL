import random
import numpy as np

class Q_Learning_Agent():

    def __init__(self, n_state, n_action, learning_rate=0.1, decay_rate = 0.5, e_greedy=0.6):
        self.lr = learning_rate
        self.epsilon = e_greedy
        self.gamma = decay_rate
        self.action = [i for i in range(n_action)]
        self.q_table = [[0 for _ in range(n_action)] for _ in range(n_state)]

    def choose(self, state, explore=True):
        if explore:
            if np.random.uniform() < self.epsilon:
                return np.argmax(self.q_table[state])
            else:
                return np.random.choice(self.action)
        else:
            return np.argmax(self.q_table[state])

    def update(self, last_state, action, state, reward):
        self.q_table[last_state][action] += self.lr * (reward + self.gamma * max(self.q_table[state]) - self.q_table[last_state][action])

class WoLF_HPC_Agent:

    def __init__(self, n_state, n_action, alpha=0.8, gamma=0.9, beta_winning=0.05, beta_losing=0.1):
        self.gamma = gamma
        self.alpha = alpha
        self.beta_losing = beta_losing
        self.beta_winning = beta_winning
        self.s_count = [0 for _ in range(n_state)]
        self.q_table = [[0 for _ in range(n_action)] for _ in range(n_state)]
        initial_prob = 1 / n_action
        self.policy = [[initial_prob for _ in range(n_action)] for _ in range(n_state)]
        self.aver_policy = [[initial_prob for _ in range(n_action)] for _ in range(n_state)]

    def choose(self, state):
        x = random.uniform(0, 1)
        for idx, action_prob in enumerate(self.policy[state]):
            x -= action_prob
            if x <= 0:
                return idx
        return len(self.policy[state]) - 1

    def update(self, p_state, action, n_state, reward):
        self.q_table[p_state][action] = (
            1 - self.alpha) * self.q_table[p_state][action] + self.alpha * (reward + self.gamma * max(self.q_table[n_state]))
        self.s_count[n_state] = self.s_count[n_state] + 1
        for idx, action_prob in enumerate(self.aver_policy[p_state]):
            self.aver_policy[p_state][idx] = self.aver_policy[p_state][idx] + \
                (1 / self.s_count[p_state]) * (self.policy[p_state]
                                               [idx] - self.aver_policy[p_state][idx])
        this_policy_reward = 0
        aver_policy_reward = 0
        for idx, q_value in enumerate(self.q_table[p_state]):
            this_policy_reward += q_value * self.policy[p_state][idx]
            aver_policy_reward += q_value * \
                self.aver_policy[p_state][idx]

        if this_policy_reward > aver_policy_reward:
            beta = self.beta_winning
        else:
            beta = self.beta_losing

        max_idx = 0
        max_val = self.q_table[p_state][0]
        for idx, q_value in enumerate(self.q_table[p_state]):
            if q_value > max_val:
                max_idx = idx
        tmp = self.policy[p_state][max_idx] + beta
        self.policy[p_state][max_idx] = min(tmp, 1)
        for idx, action_prob in enumerate(self.policy[p_state]):
            if idx != max_idx:
                tmp = self.policy[p_state][idx] + \
                    ((-beta) / (len(self.policy[p_state]) - 1))
                self.policy[p_state][idx] = max(tmp, 0)