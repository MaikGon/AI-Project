# prob.py
# This is

import random
import numpy as np

from gridutil import *

best_turn = {('N', 'E'): 'turnright',
             ('N', 'S'): 'turnright',
             ('N', 'W'): 'turnleft',
             ('E', 'S'): 'turnright',
             ('E', 'W'): 'turnright',
             ('E', 'N'): 'turnleft',
             ('S', 'W'): 'turnright',
             ('S', 'N'): 'turnright',
             ('S', 'E'): 'turnleft',
             ('W', 'N'): 'turnright',
             ('W', 'E'): 'turnright',
             ('W', 'S'): 'turnleft'}


class LocAgent:

    def __init__(self, size, walls, eps_perc, eps_move):
        self.size = size
        self.walls = walls
        # list of valid locations
        self.locations = list({*locations(self.size)}.difference(self.walls))
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.eps_perc = eps_perc
        self.eps_move = eps_move

        # previous action
        self.prev_action = None

        prob = (1.0 / (len(self.locations) * 4))
        self.P = prob * np.ones([len(self.locations), 4], dtype=np.float)
        self.move_arr = []
    def __call__(self, percept):
        arr = np.zeros([42, 42], dtype=np.float)  # location
        arr_2 = np.zeros([42, 4], dtype=np.float)  # sensor
        arr_3 = np.zeros([4, 4], dtype=np.float)  # orientation
        directions = ['N', 'E', 'S', 'W']
        perceptions = ['fwd', 'bckwd', 'left', 'right']

        if self.prev_action is not None:
            if self.prev_action == 'forward':
                for i in range(4):
                    arr_3[i][i] = 1.0

                if 'bump' in percept:
                    for i in range(42):
                        arr[i][i] = 1.0
                else:
                    for ind, val in enumerate(self.locations):
                        cnt = 4
                        loc_list = []
                        for idx, dir in enumerate(directions):
                            if dir == 'N':
                                ret_loc = (val[0], val[1] + 1)
                            elif dir == 'E':
                                ret_loc = (val[0] + 1, val[1])
                            elif dir == 'W':
                                ret_loc = (val[0] - 1, val[1])
                            elif dir == 'S':
                                ret_loc = (val[0], val[1] - 1)

                            if (ret_loc[0] < 0 or ret_loc[0] >= 16) or ret_loc in self.walls:
                                cnt -= 1
                            else:
                                x = self.loc_to_idx[ret_loc]
                                loc_list.append(x)

                        if 4 >= cnt > 0:
                            for loc in loc_list:
                                arr[ind][loc] = 0.95 / cnt
                            arr[ind][ind] = 0.05
                        elif cnt == 0:
                            arr[ind][ind] = 0.0

            elif self.prev_action == 'turnright':
                for i in range(42):
                    arr[i][i] = 1.0

                for ind, dir in enumerate(directions):
                    if dir == 'N':
                        cur_dir = 'E'
                        arr_3[ind][ind+1] = 0.95
                        arr_3[ind][ind] = 0.05
                    elif dir == 'E':
                        cur_dir = 'S'
                        arr_3[ind][ind + 1] = 0.95
                        arr_3[ind][ind] = 0.05
                    elif dir == 'S':
                        cur_dir = 'W'
                        arr_3[ind][ind + 1] = 0.95
                        arr_3[ind][ind] = 0.05
                    elif dir == 'W':
                        cur_dir = 'N'
                        arr_3[ind][0] = 0.95
                        arr_3[ind][ind] = 0.05

            elif self.prev_action == 'turnleft':
                for i in range(42):
                    arr[i][i] = 1.0

                for ind, dir in enumerate(directions):
                    if dir == 'N':
                        #cur_dir = 'W'
                        arr_3[ind][3] = 0.95
                        arr_3[ind][ind] = 0.05
                    elif dir == 'E':
                        #cur_dir = 'N'
                        arr_3[ind][ind - 1] = 0.95
                        arr_3[ind][ind] = 0.05
                    elif dir == 'S':
                        #cur_dir = 'E'
                        arr_3[ind][ind - 1] = 0.95
                        arr_3[ind][ind] = 0.05
                    elif dir == 'W':
                        #cur_dir = 'S'
                        arr_3[ind][ind - 1] = 0.95
                        arr_3[ind][ind] = 0.05
            else:
                pass

            for ind, val in enumerate(self.locations):
                for dir_ind, dir in enumerate(directions):
                    count = 1.0
                    for sens in perceptions:
                        if dir == "N":
                            if sens == 'fwd':
                                ret_loc = (val[0], val[1] + 1)
                            elif sens == 'bckwd':
                                ret_loc = (val[0], val[1] - 1)
                            elif sens == 'left':
                                ret_loc = (val[0] - 1, val[1])
                            elif sens == 'right':
                                ret_loc = (val[0] + 1, val[1])

                            if (ret_loc in self.walls or ret_loc[0] < 0 or ret_loc[0] >= 16 and sens in percept) or (
                                    ret_loc not in self.walls and 0 <= ret_loc[0] < 16 and sens not in percept):
                                count *= 0.9

                            elif (ret_loc in self.walls or ret_loc[0] < 0 or ret_loc[
                                0] >= 16 and sens not in percept) or (
                                    ret_loc not in self.walls and 0 <= ret_loc[0] < 16 and sens in percept):
                                count *= 0.1

                        elif dir == "E":
                            if sens == 'fwd':
                                ret_loc = (val[0] + 1, val[1])
                            elif sens == 'bckwd':
                                ret_loc = (val[0] - 1, val[1])
                            elif sens == 'left':
                                ret_loc = (val[0], val[1] + 1)
                            elif sens == 'right':
                                ret_loc = (val[0], val[1] - 1)

                            if (ret_loc in self.walls or ret_loc[0] < 0 or ret_loc[0] >= 16 and sens in percept) or (
                                    ret_loc not in self.walls and 0 <= ret_loc[0] < 16 and sens not in percept):
                                count *= 0.9

                            elif (ret_loc in self.walls or ret_loc[0] < 0 or ret_loc[
                                0] >= 16 and sens not in percept) or (
                                    ret_loc not in self.walls and 0 <= ret_loc[0] < 16 and sens in percept):
                                count *= 0.1

                        elif dir == "S":
                            if sens == 'fwd':
                                ret_loc = (val[0], val[1] - 1)
                            elif sens == 'bckwd':
                                ret_loc = (val[0], val[1] + 1)
                            elif sens == 'left':
                                ret_loc = (val[0] + 1, val[1])
                            elif sens == 'right':
                                ret_loc = (val[0] - 1, val[1])

                            if (ret_loc in self.walls or ret_loc[0] < 0 or ret_loc[0] >= 16 and sens in percept) or (
                                    ret_loc not in self.walls and 0 <= ret_loc[0] < 16 and sens not in percept):
                                count *= 0.9

                            elif (ret_loc in self.walls or ret_loc[0] < 0 or ret_loc[
                                0] >= 16 and sens not in percept) or (
                                    ret_loc not in self.walls and 0 <= ret_loc[0] < 16 and sens in percept):
                                count *= 0.1

                        elif dir == "W":
                            if sens == 'fwd':
                                ret_loc = (val[0] - 1, val[1])
                            elif sens == 'bckwd':
                                ret_loc = (val[0] + 1, val[1])
                            elif sens == 'left':
                                ret_loc = (val[0], val[1] - 1)
                            elif sens == 'right':
                                ret_loc = (val[0], val[1] + 1)

                            if (ret_loc in self.walls or ret_loc[0] < 0 or ret_loc[0] >= 16 and sens in percept) or (
                                    ret_loc not in self.walls and 0 <= ret_loc[0] < 16 and sens not in percept):
                                count *= 0.9

                            elif (ret_loc in self.walls or ret_loc[0] < 0 or ret_loc[
                                0] >= 16 and sens not in percept) or (
                                    ret_loc not in self.walls and 0 <= ret_loc[0] < 16 and sens in percept):
                                count *= 0.1

                    arr_2[ind][dir_ind] = count

            arr_t = np.transpose(arr)

            temp_P = np.multiply(np.dot(np.dot(arr_t, self.P), arr_3), arr_2)
            self.P = temp_P / temp_P.sum()

        action = 'forward'

        if len(self.move_arr) > 8 and (''.join(self.move_arr[-8:]) == 'turnleftforwardturnleftforwardturnleftforwardturnleftforward' or ''.join(self.move_arr[-8:]) == 'forwardturnleftforwardturnleftforwardturnleftforwardturnleft'):
            # if agent will perform 4, the same moves (turnleft, forward), try to get out of the loop
            action = 'turnright'

        else:
            # if there is an option, turn left or stick to the left wall
            if (self.prev_action == 'turnleft' or self.prev_action == 'turnright') and 'fwd' not in percept:
                action = 'forward'
            elif 'left' not in percept:
                action = 'turnleft'
            elif 'left' in percept and 'right' in percept and 'fwd' in percept:
                action = 'turnleft'
            elif 'fwd' not in percept:
                action = 'forward'
            else:
                action = 'turnright'

        self.move_arr.append(action)

        self.prev_action = action

        return action

    def getPosterior(self):
        P_arr = np.zeros([self.size, self.size, 4], dtype=np.float)
        for idx, loc in enumerate(self.locations):
            for i in range(4):
                P_arr[loc[0], loc[1], i] = self.P[idx][i]

        return P_arr

    def forward(self, cur_loc, cur_dir):
        if cur_dir == 'N':
            ret_loc = (cur_loc[0], cur_loc[1] + 1)
        elif cur_dir == 'E':
            ret_loc = (cur_loc[0] + 1, cur_loc[1])
        elif cur_dir == 'W':
            ret_loc = (cur_loc[0] - 1, cur_loc[1])
        elif cur_dir == 'S':
            ret_loc = (cur_loc[0], cur_loc[1] - 1)
        ret_loc = (min(max(ret_loc[0], 0), self.size - 1), min(max(ret_loc[1], 0), self.size - 1))
        return ret_loc, cur_dir

    def backward(self, cur_loc, cur_dir):
        if cur_dir == 'N':
            ret_loc = (cur_loc[0], cur_loc[1] - 1)
        elif cur_dir == 'E':
            ret_loc = (cur_loc[0] - 1, cur_loc[1])
        elif cur_dir == 'W':
            ret_loc = (cur_loc[0] + 1, cur_loc[1])
        elif cur_dir == 'S':
            ret_loc = (cur_loc[0], cur_loc[1] + 1)
        ret_loc = (min(max(ret_loc[0], 0), self.size - 1), min(max(ret_loc[1], 0), self.size - 1))
        return ret_loc, cur_dir

    @staticmethod
    def turnright(cur_loc, cur_dir):
        dir_to_idx = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        dirs = ['N', 'E', 'S', 'W']
        idx = (dir_to_idx[cur_dir] + 1) % 4
        return cur_loc, dirs[idx]

    @staticmethod
    def turnleft(cur_loc, cur_dir):
        dir_to_idx = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        dirs = ['N', 'E', 'S', 'W']
        idx = (dir_to_idx[cur_dir] + 4 - 1) % 4
        return cur_loc, dirs[idx]
