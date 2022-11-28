import gym
import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Convolution2D, Dropout, MaxPooling2D
from tensorflow.keras.optimizers import Adam
from collections import deque
from keras.callbacks import TensorBoard
import time
REPLAY_MEMORY_SIZE = 50_000
MIN_REPLAY_MEMORY_SIZE = 1_000
MINIBATCH_SIZE=64
MODEL_NAME="ATARi"
class ModifiedTensorBoard(TensorBoard):

    # Overriding init to set initial step and writer (we want one log file for all .fit() calls)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.step = 1
        self.writer = tf.summary.FileWriter(self.log_dir)

    # Overriding this method to stop creating default log writer
    def set_model(self, model):
        pass

    # Overrided, saves logs with our step number
    # (otherwise every .fit() will start writing from 0th step)
    def on_epoch_end(self, epoch, logs=None):
        self.update_stats(**logs)

    # Overrided
    # We train for one batch only, no need to save anything at epoch end
    def on_batch_end(self, batch, logs=None):
        pass

    # Overrided, so won't close writer
    def on_train_end(self, _):
        pass

    # Custom method for saving own metrics
    # Creates writer, writes custom metrics and closes writer
    def update_stats(self, **stats):
        self._write_logs(stats, self.step)

class DQNAgent:
    def __init__(self):
        self.env = gym.make("ALE/Assault-v5")
        # main model
        self.model = self.create_model(self.env.observation_space.shape, self.env.action_space.n)
        # target_model
        self.target_model = self.create_model(self.env.observation_space.shape, self.env.action_space.n)
        self.target_model.set_weights(self.model.get_weights())
        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)
        # Custom tensorboard object
        self.tensorboard = ModifiedTensorBoard(log_dir="logs/{}-{}".format(MODEL_NAME, int(time.time())))

        # Used to count when to update target network with main network's weights
        self.target_update_counter = 0
    def create_model(self, OBSERVATION_SPACE, ACTION_SPACE_SIZE):
        model = Sequential()
        model.add(Convolution2D(256, (3, 3), activation='relu', input_shape=OBSERVATION_SPACE))
        model.add(MaxPooling2D(2, 2))
        model.add(Dropout(0.2))

        model.add(Convolution2D(256, (3, 3), activation='relu'))
        model.add(MaxPooling2D(2, 2))
        model.add(Dropout(0.2))

        model.add(Flatten())
        model.add(Dense(64))
        model.add(Dense(ACTION_SPACE_SIZE))
        model.compile(loss="mse", optimizer=Adam(learning_rate=0.001), metrics=['accuracy'])
        return model
    def update_replay_memory(self,transition):
        self.replay_memory.append(transition)
    def get_qs(self,state,step):
        return self.model.predict(np.array(state).reshape(-1, *state.shape)/255)[0]
    def train(self, terminal_state,step):
        if len(self.replay_memory)<MIN_REPLAY_MEMORY_SIZE:
            return
        mini_bach=random.sample(self.replay_memory,MINIBATCH_SIZE)
        current_state=np.array([transition[0] for transition in mini_bach])/255
        current_qs_list=self.model.predict(current_state)

        new_current_states=np.array([transition[3] for transition in mini_bach])/255
        future_qs_list=self.target_model.predict(new_current_states)

        X=[]
        Y=[]


agent = DQNAgent()
