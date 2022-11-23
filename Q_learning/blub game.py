import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time

style.use("ggplot")
SIZE = 10
HM_EPISODES = 25000
MOVE_PENALTY = 1
ENEMY_PENALTY = 350
FOOD_REWARD = 25
epsilon = 0.7  # randomness
EPS_DECAY = 0.9999
SHOW_EVERY = 1000
start_q_table = None #  # if we have a pickled Q table, we'll put the filename of it here.
LEARNING_RATE = 0.1
DISCOUNT = 0.95

PLAYER_N = 1  # player key in dict
FOOD_N = 2  # food key in dict
ENEMY_N = 3  # enemy key in dict

# the dict! Using just for colors
d = {1: (255, 0, 0),  # blueish color
     2: (0, 255, 0),  # green
     3: (0, 0, 255)}  #


class Blob:
    def __init__(self):
        self.x = np.random.randint(0, SIZE)
        self.y = np.random.randint(0, SIZE)
    def __str__(self):
        return f"{self.x}, {self.y}"
    def __sub__(self, other):
        return (self.x - other.x, self.y - other.y)
    def action(self, choice):
        # if choice==0: # Forwrd
        #     self.move(1,0)
        # if choice==1: # backwards
        #     self.move(-1,0)
        # if choice==2: # Up
        #     self.move(0,-1)
        # if choice==3: # Down
        #     self.move(0,1)
        if choice==0: # UP & Forward
            self.move(1,-1)
        if choice==1: # UP & Backwards
            self.move(-1,-1)
        if choice==2: # Down & Forward
            self.move(1,1)
        if choice==3: # Down & Backwards
            self.move(-1,1)
    def move(self,x=False,y=False):
        if not x:
            self.x += np.random.randint(-1, 2)
        else:
            self.x +=x
        if not y:
            self.y += np.random.randint(-1, 2)
        else:
            self.y +=y
        # If we are out of bounds, fix!
        if self.x < 0:
            self.x = 0
        elif self.x > SIZE - 1:
            self.x = SIZE - 1
        if self.y < 0:
            self.y = 0
        elif self.y > SIZE - 1:
            self.y = SIZE - 1


if start_q_table is None:
    # initialize the q-table#
    q_table = {}
    for i in range(-SIZE+1, SIZE):
        for ii in range(-SIZE+1, SIZE):
            for iii in range(-SIZE+1, SIZE):
                    for iiii in range(-SIZE+1, SIZE):
                        q_table[((i, ii), (iii, iiii))] = [np.random.uniform(-5, 0) for i in range(4)]
    print("done with initiale Qtable")
else:
    with open(start_q_table, "rb") as f:
        q_table = pickle.load(f)

episode_rewards = []

for episode in range(HM_EPISODES):
    player = Blob()
    food = Blob()
    enemy = Blob()
    if episode % SHOW_EVERY == 0:
        print(f"on #{episode}, epsilon is {epsilon}")
        print(f"{SHOW_EVERY} ep mean: {np.mean(episode_rewards[-SHOW_EVERY:])}")
        show = True
    else:
        show = False
    episode_reward = 0
    for i in range(200):
        obs = (player - food, player - enemy)
        if np.random.random() > epsilon:
            action = np.argmax(q_table[obs])
        else:
            action = np.random.randint(0, 4)
        player.action(action)
        enemy.move()
        #food.move()
        if player.x == enemy.x and player.y == enemy.y:
            reward = -ENEMY_PENALTY
            print("elbess")
        elif player.x == food.x and player.y == food.y:
            reward = FOOD_REWARD
            print("Sa77a")
        else:
            reward = -MOVE_PENALTY
        new_obs = (player - food, player - enemy)  # new observation
        max_future_q = np.max(q_table[new_obs])  # max Q value for this new obs
        current_q = q_table[obs][action]  # current Q for our chosen action
        if reward == FOOD_REWARD:
            new_q = FOOD_REWARD
        else:
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
        if show:
            env = cv2.imread("background photos/img1.png")
            env = cv2.resize(env, (SIZE, SIZE), interpolation = cv2.INTER_AREA)
            env[food.x][food.y] = d[FOOD_N]  # sets the food location tile to green color
            env[player.x][player.y] = d[PLAYER_N]  # sets the player tile to blue
            env[enemy.x][enemy.y] = d[ENEMY_N]  # sets the enemy location to red
            #img = Image.fromarray(env, 'RGB')  # reading to rgb. Apparently. Even tho color definitions are bgr. ???
            #img = img.resize((300, 300))  # resizing so we can see our agent in all its glory.
            #cv2.imshow("image", np.array(img))  # show it!
            env = cv2.resize(env, (200, 200), interpolation = cv2.INTER_AREA)
            cv2.imshow("dd",env)
            if reward == FOOD_REWARD or reward == -ENEMY_PENALTY:  # crummy code to hang at the end if we reach abrupt end for good reasons or not.
                if cv2.waitKey(500) & 0xFF == ord('q'):
                    break
            else:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        episode_reward += reward
        if reward == FOOD_REWARD or reward == -ENEMY_PENALTY:
            break
    # print(episode_reward)
    episode_rewards.append(episode_reward)
    epsilon *= EPS_DECAY

moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')
plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f"Reward {SHOW_EVERY}ma")
plt.xlabel("episode #")
plt.show()

with open(f"qtable-{int(time.time())}.pickle", "wb") as f:
    pickle.dump(q_table, f)