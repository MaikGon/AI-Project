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

        self.turn_move_prob = 1 - eps_move  # probability of turning or moving
        self.obs_prob = 1 - eps_perc  # probability of correctly sensed obstacles
        self.num_locations = len(self.locations)  # number of locations
        self.num_orientations = 4  # number of orientations

        prob = (1.0 / (len(self.locations) * 4))
        self.P = prob * np.ones([len(self.locations), 4], dtype=np.float)
        self.move_arr = []

    def __call__(self, percept):
        arr_loc = np.zeros([self.num_locations, self.num_locations], dtype=np.float)  # location
        arr_sensor = np.zeros([self.num_locations, self.num_orientations], dtype=np.float)  # sensor
        arr_orient = np.zeros([self.num_orientations, self.num_orientations], dtype=np.float)  # orientation

        heur_arr = []  # to help agent leave the loop of four the same moves (in heuristics)
        for i in range(4):
            heur_arr.append('turnleftforward')

        directions = ['N', 'E', 'S', 'W']
        perceptions = ['fwd', 'bckwd', 'left', 'right']

        if self.prev_action is not None:
            if self.prev_action == 'forward':
                for i in range(self.num_orientations):
                    arr_orient[i][i] = 1.0

                if 'bump' in percept:
                    for i in range(self.num_locations):
                        arr_loc[i][i] = 1.0
                else:
                    for ind, val in enumerate(self.locations):
                        cnt = 4  # counts how many free spaces there are around the agent - 4 means no walls
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

                            if ret_loc[0] < 0 or ret_loc[0] >= self.size or ret_loc in self.walls:
                                cnt -= 1
                            else:
                                x = self.loc_to_idx[ret_loc]
                                loc_list.append(x)

                        if cnt != 0:
                            for loc in loc_list:
                                # divide the probability of moving forward by number of free spaces around the agent
                                arr_loc[ind][loc] = self.turn_move_prob / cnt
                            arr_loc[ind][ind] = self.eps_move

            elif self.prev_action == 'turnright':
                for i in range(self.num_locations):
                    arr_loc[i][i] = 1.0

                for ind, dir in enumerate(directions):
                    if dir == 'N':
                        arr_orient[ind][ind+1] = self.turn_move_prob
                    elif dir == 'E':
                        arr_orient[ind][ind + 1] = self.turn_move_prob
                    elif dir == 'S':
                        arr_orient[ind][ind + 1] = self.turn_move_prob
                    elif dir == 'W':
                        arr_orient[ind][0] = self.turn_move_prob
                    arr_orient[ind][ind] = self.eps_move

            elif self.prev_action == 'turnleft':
                for i in range(self.num_locations):
                    arr_loc[i][i] = 1.0

                for ind, dir in enumerate(directions):
                    if dir == 'N':
                        arr_orient[ind][3] = self.turn_move_prob
                    elif dir == 'E':
                        arr_orient[ind][ind - 1] = self.turn_move_prob
                    elif dir == 'S':
                        arr_orient[ind][ind - 1] = self.turn_move_prob
                    elif dir == 'W':
                        arr_orient[ind][ind - 1] = self.turn_move_prob
                    arr_orient[ind][ind] = self.eps_move

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

                            count = self.count_sens_prob(count, ret_loc, sens, percept)

                        elif dir == "E":
                            if sens == 'fwd':
                                ret_loc = (val[0] + 1, val[1])
                            elif sens == 'bckwd':
                                ret_loc = (val[0] - 1, val[1])
                            elif sens == 'left':
                                ret_loc = (val[0], val[1] + 1)
                            elif sens == 'right':
                                ret_loc = (val[0], val[1] - 1)

                            count = self.count_sens_prob(count, ret_loc, sens, percept)

                        elif dir == "S":
                            if sens == 'fwd':
                                ret_loc = (val[0], val[1] - 1)
                            elif sens == 'bckwd':
                                ret_loc = (val[0], val[1] + 1)
                            elif sens == 'left':
                                ret_loc = (val[0] + 1, val[1])
                            elif sens == 'right':
                                ret_loc = (val[0] - 1, val[1])

                            count = self.count_sens_prob(count, ret_loc, sens, percept)

                        elif dir == "W":
                            if sens == 'fwd':
                                ret_loc = (val[0] - 1, val[1])
                            elif sens == 'bckwd':
                                ret_loc = (val[0] + 1, val[1])
                            elif sens == 'left':
                                ret_loc = (val[0], val[1] - 1)
                            elif sens == 'right':
                                ret_loc = (val[0], val[1] + 1)

                            count = self.count_sens_prob(count, ret_loc, sens, percept)

                    arr_sensor[ind][dir_ind] = count

            temp_P = np.multiply(np.dot(np.dot(np.transpose(arr_loc), self.P), arr_orient), arr_sensor)
            self.P = temp_P / temp_P.sum()

        if len(self.move_arr) >= 8 and ''.join(self.move_arr[-8:]) == ''.join(heur_arr):
            # if agent will perform 4, the same moves (turnleft, forward), try to escape the loop
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

    def count_sens_prob(self, count, ret_loc, sens, percept):
        var_fir, var_sec = False, False
        if ret_loc in self.walls or ret_loc[0] < 0 or ret_loc[0] >= self.size:  # check if this position is in the wall or outside the map
            var_fir = True
        if ret_loc not in self.walls and 0 <= ret_loc[0] < self.size:  # check if this position is in the allowed location
            var_sec = True

        if (var_fir and sens in percept) or (var_sec and sens not in percept):
            count *= self.obs_prob

        else:
            count *= self.eps_perc

        return count

    def getPosterior(self):
        P_arr = np.zeros([self.size, self.size, self.num_orientations], dtype=np.float)
        for idx, loc in enumerate(self.locations):
            for i in range(self.num_orientations):
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
