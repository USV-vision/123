# coding: utf-8
import sys
import time
import numpy as np
import pandas as pd
import numpy as np
import tkinter as tk
import random


class Maze(tk.Tk, object):
    UNIT = 40  # 像素
    MAZE_H = 6  # 网格高度
    MAZE_W = 6  # 网格宽度

    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['U', 'D', 'L', 'R']
        self.n_actions = len(self.action_space)
        self.title('迷宫')
        self.geometry('{0}x{1}'.format(self.MAZE_H * self.UNIT,
                                       self.MAZE_W * self.UNIT))
        self._build_maze()

    # 画矩形
    # x y 格坐标
    # color 颜色
    def _draw_rect(self, x, y, color):
        center = self.UNIT / 2
        w = center - 5
        x_ = self.UNIT * x + center
        y_ = self.UNIT * y + center
        return self.canvas.create_rectangle(x_ - w,
                                            y_ - w,
                                            x_ + w,
                                            y_ + w,
                                            fill=color)

    # 初始化迷宫
    def _build_maze(self):
        h = self.MAZE_H * self.UNIT
        w = self.MAZE_W * self.UNIT
        # 初始化画布
        self.canvas = tk.Canvas(self, bg='white', height=h, width=w)
        # 画线
        for c in range(0, w, self.UNIT):
            self.canvas.create_line(c, 0, c, h)
        for r in range(0, h, self.UNIT):
            self.canvas.create_line(0, r, w, r)

        # 陷阱
        self.hells = [
            self._draw_rect(3, 2, 'black'),
            self._draw_rect(3, 3, 'black'),
            self._draw_rect(3, 4, 'black'),
            self._draw_rect(3, 5, 'black'),
            self._draw_rect(4, 5, 'black'),
            self._draw_rect(1, 0, 'black'),
            self._draw_rect(1, 1, 'black'),
            self._draw_rect(1, 2, 'black'),
            self._draw_rect(1, 4, 'black'),
            self._draw_rect(3, 0, 'black')
        ]
        self.hell_coords = []
        for hell in self.hells:
            self.hell_coords.append(self.canvas.coords(hell))

        # 奖励
        self.oval = self._draw_rect(4, 5, 'yellow')
        # 玩家对象
        self.rect = self._draw_rect(0, 0, 'red')

        self.canvas.pack()  # 执行画

    # 重新初始化（用于撞到黑块后重新开始）
    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.rect)
        self.rect = self._draw_rect(0, 0, 'red')
        self.old_s = None
        # 返回 玩家矩形的坐标 [5.0, 5.0, 35.0, 35.0]
        return self.canvas.coords(self.rect)

    # 走下一步
    def step(self, action):
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action == 0:  # up
            if s[1] > self.UNIT:
                base_action[1] -= self.UNIT
        elif action == 1:  # down
            if s[1] < (self.MAZE_H - 1) * self.UNIT:
                base_action[1] += self.UNIT
        elif action == 2:  # right
            if s[0] < (self.MAZE_W - 1) * self.UNIT:
                base_action[0] += self.UNIT
        elif action == 3:  # left
            if s[0] > self.UNIT:
                base_action[0] -= self.UNIT

        # 根据策略移动红块
        # self.canvas.move(self.rect, base_action[0], base_action[1])
        s_ = self.canvas.coords(self.rect)

        # 判断是否得到奖励或惩罚
        done = False
        if s_ == self.canvas.coords(self.oval):
            reward = 1
            done = True
        elif s_ in self.hell_coords:
            reward = -1
            done = True
        # elif base_action.sum() == 0:
        #    reward = -1
        else:
            reward = 0

        self.old_s = s
        return reward, done, base_action[0], base_action[1]

    def render(self):
        time.sleep(0.01)
        self.update()


if __name__ == "__main__":
    env = Maze()
    while True:
        d1 = False
        p1 = []
        p2 = []
        for action in range(4):
            r, done, a, b = env.step(action)
            d11 = False
            if done:
                d11 = True
                break
            if r == 0 & a < 200 & b < 240:
                p1.append(a)
                p2.append(b)
                print(p1)
        d1 = d11
        if d1:
            break
        d_1 = []
        for m in range(len(p1)):
            D = (p1[m] / 40 - 4)**2 + (p2[m] / 40 - 5)**2
            d_1.append(D)
        max_d = min(d_1)
        print(d_1)
        max_m = d_1.index(max_d)
        ran = random.random()
        if ran > 0.2:
            env.canvas.move(env.rect, p1[max_m], p2[max_m])
        else:
            ran1 = random.randint(0, len(p1) - 1)
            env.canvas.move(env.rect, p1[ran1], p2[ran1])
        env.render()
        time.sleep(1)


    # env.canvas.move(env.rect, p1[0], p2[0])
    # env.render()
    # env.mainloop()
