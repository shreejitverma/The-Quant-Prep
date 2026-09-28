#
# Deep Q-Learning Agent
#
# (c) Dr. Yves J. Hilpisch
# Reinforcement Learning for Finance
#

import os
import random
import warnings
import numpy as np
import tensorflow as tf
from tensorflow import keras
from collections import deque
from keras.layers import Dense
from keras.models import Sequential

warnings.simplefilter('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from tensorflow.python.framework.ops import disable_eager_execution
disable_eager_execution()

opt = keras.optimizers.legacy.Adam(learning_rate=0.0001)


class DQLAgent:
    def __init__(self, symbol, feature, n_features, env, hu=24):
        self.epsilon = 1.0
        self.epsilon_decay = 0.9975
        self.epsilon_min = 0.1
        self.memory = list()
        self.batch_size = 32
        self.gamma = 0.5
        self.trewards = deque(maxlen=2000)
        self.max_treward = 0
        self.n_features = n_features
        self.env = env
        self._create_model(hu)

    def _create_model(self, hu):
        self.model = Sequential()
        self.model.add(Dense(hu, activation='relu',
                             input_dim=self.n_features))
        self.model.add(Dense(hu, activation='relu'))
        self.model.add(Dense(2, activation='linear'))
        self.model.compile(loss='mse', optimizer=opt)

    def _reshape(self, state):
        if state.ndim == 1:
            return np.reshape(state, [1, self.n_features])
        elif state.ndim == 2:
            return np.reshape(state, [1, state.shape[0], state.shape[1]])
        else:
            return state

    def act(self, state):
        if random.random() < self.epsilon:
            return self.env.action_space.sample()
        return np.argmax(self.model.predict(state)[0])

    def replay(self):
        batch = random.sample(self.memory, self.batch_size)
        for state, action, next_state, reward, done in batch:
            # print(next_state)
            if not done:
                if next_state.ndim == 1:
                    reward += self.gamma * np.amax(
                        self.model.predict(self._reshape(next_state)[0]))
                else:
                    reward += self.gamma * np.amax(
                        self.model.predict(self._reshape(next_state))[0, 0])
            target = self.model.predict(self._reshape(state))
            target[0, action] = reward
            self.model.fit(state, target, epochs=1, verbose=False)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def learn(self, episodes):
        for e in range(1, episodes + 1):
            state, _ = self.env.reset()
            state = self._reshape(state)
            for f in range(1, 5000):
                action = self.act(state)
                next_state, reward, done, trunc, _ = self.env.step(action)
                next_state = self._reshape(next_state)
                self.memory.append(
                    [state, action, next_state, reward, done])
                state = next_state
                if done:
                    self.trewards.append(f)
                    self.max_treward = max(self.max_treward, f)
                    templ = f'episode={e:4d} | treward={f:4d}'
                    templ += f' | max={self.max_treward:4d}'
                    print(templ, end='\r')
                    break
            if len(self.memory) > self.batch_size:
                self.replay()
        print()

    def test(self, episodes):
        ma = self.env.min_accuracy
        self.env.min_accuracy = 0.5
        for e in range(1, episodes + 1):
            state, _ = self.env.reset()
            state = self._reshape(state)
            for f in range(1, 5001):
                action = np.argmax(self.model.predict(state)[0])
                state, reward, done, trunc, _ = self.env.step(action)
                state = self._reshape(state)
                if done:
                    print(f'total reward={f:4d} | accuracy={self.env.accuracy:.3f}')
                    break
        self.env.min_accuracy = ma
