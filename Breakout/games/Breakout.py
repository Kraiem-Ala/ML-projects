import pygame
import cv2
import time
import random


class yajour():
    def __init__(self, level, factor):
        self.factor = factor
        self.level = level
        self.colors = [(0, 0, 0), (0, 255, 127), (0, 191, 255), (255, 99, 71)]
        self.block = []
        self.rects = []

    def wall(self, rows, cols):
        self.height = int((80* self.factor)/rows)
        self.width = int((200* self.factor)/cols)
        for row in range(rows):
            block_row = []
            block1=[]
            for col in range(cols):
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                if row == rows - 1:
                    strength = self.level
                elif row == rows - 2:
                    strength = self.level + 1
                    if strength > 2:
                        strength = 2
                else:
                    strength = self.level + 2
                    if strength > 3:
                        strength = 3
                self.rects.append(rect)
                block = [rect, strength]
                block_row.append(block)
            self.block.append(block_row)


    def reset(self):
        self.block = []


class badlle(object):
    def __init__(self, factor):
        super(badlle, self).__init__()
        self.factor = factor
        self.height = 10 * self.factor
        self.width = 30 * self.factor
        self.color = (0, 0, 0)
        self.x = int(((200 * self.factor) / 2) - self.width / 2)
        self.y = int((200 * self.factor) - self.height / 2)
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.diretion = 0

    def move(self, action):
        if action == 1:
            self.x += self.speed
            if (self.x + self.width) > (200 * self.factor):
                self.x = (200 * self.factor) - self.width
        elif action == 0:
            self.x -= self.speed
            if self.x < 0:
                self.x = 0
        else:
            pass
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def get_action(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.move(0)
        elif key[pygame.K_RIGHT]:
            self.move(1)
        else:
            pass
    def reset(self):
        self.x = int(((200 * self.factor) / 2) - self.width / 2)
        self.y = int((200 * self.factor) - self.height / 2)
    def draw_paddle(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)


class ball(object):
    def __init__(self, factor, level):
        super(ball, self).__init__()
        self.direction_x = random.choice([1,-1])
        self.direction_y = 1
        self.ball_image = pygame.image.load(f"C:/Users/Kraiem Ala Eddine/Desktop/Machine learning tuto/ML-project/Breakout/games/ball_games/{factor * 200}/ball{level}.png")
        if factor==2:
            self.size_x=20
            self.size_y=20
        else:
            self.size_x = 10
            self.size_y = 10
        self.pos_x = int((200 * factor) / 2)
        self.pos_y = int((200 * factor) / 2)
        self.speed_x = 2+level
        self.speed_y = 2+level
        self.factor = factor
        self.rect=pygame.Rect(self.pos_x, self.pos_y, self.size_x, self.size_y)

    def draw(self,screen):
        self.move()
        screen.blit(self.ball_image, (self.pos_x, self.pos_y))
        #pygame.draw.rect(screen, (0,0,0), self.rect)

    def move(self):
        self.pos_x += (self.speed_x * self.direction_x)
        self.pos_y += (self.speed_y * self.direction_y)
        self.rect.move_ip(self.speed_x*self.direction_x,self.speed_y*self.direction_y)
    def reset(self):
         self.direction_x = 1
         self.direction_y = 1
         self.pos_x = int((200 * self.factor) / 2)
         self.pos_y = int((200 * self.factor) / 2)
         self.rect = pygame.Rect(self.pos_x, self.pos_y, self.size_x, self.size_y)



class breakout(object):
    """docstring for breakout"""

    def __init__(self, width=200, height=200):
        #super(breakout, self).__init__()
        pygame.init()
        self.tries=5
        self.width = width
        self.height = height
        self.factor = int(self.width / 200)
        self.level = 1
        self.level_rows = 6
        self.level_col = 7
        self.blocks = yajour(self.level, self.factor)
        self.badle = badlle(self.factor)
        self.ball=ball(self.factor,self.level)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.bg = pygame.image.load(f"C:/Users/Kraiem Ala Eddine/Desktop/Machine learning tuto/ML-project/Breakout/games/background/{self.width}/level{self.level}.jpg")
        self.clock = pygame.time.Clock()
        self.fps = 50
        self.destryed_bricks=0
        pygame.display.set_caption('Breakout')

    def setup(self):
        self.ball = ball(self.factor, self.level)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.bg = pygame.image.load(f"C:/Users/Kraiem Ala Eddine/Desktop/Machine learning tuto/ML-project/Breakout/games/background/{self.width}/level{1}.jpg")
        self.badle.draw_paddle(self.screen)
        self.blocks.wall(self.level_rows, self.level_col)

    def close(self):
        pygame.quit()

    def build_wall(self, screen):
        for row in self.blocks.block:
            for block in row:
                bloc_color = self.blocks.colors[block[1]]
                pygame.draw.rect(screen, bloc_color, block[0])
                pygame.draw.rect(screen, self.blocks.colors[0], block[0], 2)

    def check_blocks(self):
        to_delete = []
        for row_i,row in enumerate(self.blocks.block):
            for block in row:
                if (block[0].bottom-3<=self.ball.rect.top<=block[0].bottom) and (block[0].left <= self.ball.rect.centerx<=block[0].right):
                    self.ball.direction_y *= -1
                    to_delete.append([row_i,row.index(block)])
                    self.destryed_bricks+=1
                elif (block[0].top-3<=self.ball.rect.bottom<=block[0].top+3) and (block[0].left <= self.ball.rect.centerx<=block[0].right):
                    #print(f"case2 block top {block[0].top} : ballbottom{self.ball.rect.bottom} ")
                    #self.ball.direction_x *= -1
                    self.ball.direction_y *= -1
                    to_delete.append([row_i,row.index(block)])
                    self.destryed_bricks+=1
                elif (block[0].right+2>=self.ball.rect.left>=block[0].right) and (block[0].top <= self.ball.rect.centery<=block[0].bottom):
                    self.ball.direction_x *= -1
                    to_delete.append([row_i,row.index(block)])
                    self.destryed_bricks+=1
                elif (block[0].left<=self.ball.rect.right<=block[0].left+2) and (block[0].top <= self.ball.rect.centery<=block[0].bottom):
                    self.ball.direction_x *= -1
                    to_delete.append([row_i,row.index(block)])
                    self.destryed_bricks+=1
        for index in to_delete:
                    #print(index)
            self.blocks.block[index[0]][index[1]][0]=pygame.Rect(0,0,0,0)

    def ball_movement(self):
        if (self.ball.pos_y >= (self.badle.y - self.badle.height)) :
            if (self.badle.x<= self.ball.pos_x <=self.badle.x+self.badle.width):
                self.ball.direction_y = -1
            elif(self.badle.rect.left <= self.ball.rect.right <= self.badle.rect.left+2) or (self.badle.rect.right - 2 <= self.ball.rect.left <= self.badle.rect.right+2):
                self.ball.direction_x *= -1
                self.ball.direction_y *= -1
            #print("touch badle")
        if (self.ball.pos_y <= 0):
            self.ball.direction_y = -1 * self.ball.direction_y
            #print("touch roof")
        if ((self.ball.pos_x <= 0)or(self.ball.pos_x >= self.width)) and (0<= self.ball.pos_y <=self.height):
            self.ball.direction_x = -1 * self.ball.direction_x
            #print("touch walls")
        if (self.ball.pos_y >= self.height):
            print("Game Over")
            return True
        self.check_blocks()
        self.ball.draw(self.screen)
        return False


    def reset_game(self,all=False):
        self.badle.reset()
        self.ball.reset()
        if all == True:
            self.blocks.block=[]
            self.blocks.wall(self.level_rows,self.level_col)
            self.destryed_bricks=0

    def render(self,level,max_tries):
        self.ball = ball(self.factor, level)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.bg = pygame.image.load(f"C:/Users/Kraiem Ala Eddine/Desktop/Machine learning tuto/ML-project/Breakout/games/background/{self.width}/level{level}.jpg")
        self.level=level
        self.blocks.wall(self.level_rows, self.level_col)
        self.badle.draw_paddle(self.screen)
        run = False
        level_done=True
        tries=0
        while not run:
            self.clock.tick(self.fps)
            self.screen.fill((255, 0, 0))
            self.screen.blit(self.bg, (0, 0))
            self.build_wall(self.screen)
            self.badle.get_action()
            self.badle.draw_paddle(self.screen)
            info=self.ball_movement()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = True
                    level_done=False
            pygame.display.update()
            if info==True :
                tries+=1
                self.reset_game()
            if tries == max_tries:
                run=True
                level_done = False
            if len(self.blocks.block) * len(self.blocks.block[0]) == self.destryed_bricks:
                win=pygame.image.load(f"C:/Users/Kraiem Ala Eddine/Desktop/Machine learning tuto/ML-project/Breakout/games/background/{self.width}/victory.jpg")
                self.screen.blit(win,(50,50))
                pygame.display.update()
                time.sleep(5)
                run=True
                level_done = True
            img=pygame.surfarray.array3d(self.screen)
        return self.destryed_bricks, level_done

    def stepping(self,action):
        level_done=False
        self.badle.move(action)
        #self.clock.tick(self.fps)
        self.screen.fill((255, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        self.build_wall(self.screen)
        self.badle.draw_paddle(self.screen)
        info = self.ball_movement()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                level_done = True
        pygame.display.update()
        if len(self.blocks.block) * len(self.blocks.block[0]) == self.destryed_bricks:
            win = pygame.image.load(f"C:/Users/Kraiem Ala Eddine/Desktop/Machine learning tuto/ML-project/Breakout/games/background/{self.width}/victory.jpg")
            self.screen.blit(win, (50, 50))
            pygame.display.update()
            time.sleep(0.5)
            level_done = True
        if info==True:
            level_done = True
        img = pygame.surfarray.array3d(self.screen)
        return img,self.destryed_bricks, level_done

    def step(self,action):
        state,score,done=self.stepping(action)
        return state,score,done

    def play_game(self):
        score, done =self.render(level=1,max_tries=4)
        print(f" SCORE = {score}")
        if done:
            score, done =self.render(level=2, max_tries=4)
            print(f" SCORE = {score}")
        if done:
            score, done =self.render(level=3, max_tries=4)
            print(f" SCORE = {score}")
        if done:
            print("Well done")
            print(f" SCORE = {score}")
        self.close()


def main():
    sequence=[]
    game = breakout(width=400, height=400)
    game.setup()
    #game.play_game()
    for _ in range (10):
        done = False
        while not done:
            action=random.choice([0,1])
            state,score,done=game.step(action)
        print(f"Score on episode {score}")
        game.reset_game(all=True)
    # # for i,image in enumerate(sequence):
    # #     cv2.imshow(f"image {i}", image)
    # # cv2.waitKey(0)
