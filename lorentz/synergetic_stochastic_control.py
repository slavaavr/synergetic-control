import numpy as np
import random as rand
from typing import List
import matplotlib.pyplot as plt
from regr.nadaray_watson import NW
from lorentz.lorentz_model_states import *
from mpl_toolkits.mplot3d import Axes3D


class EquationSystem:
    x: float
    y: float
    y_prev: float
    z: float
    z_prev: float

    is_controllable: bool
    is_filter_enabled: bool
    noise: float
    noise_1: float
    noise_math_expectation = 0
    noise_standard_deviation: float
    # -----------------------------
    a1: float
    a2: float
    a3: float
    a4: float
    a5: float
    a6: float

    t0: float
    u_max: float
    c: float
    T: float
    p: float
    # -----------------------------
    x_arr: List[float]
    y_arr: List[float]
    z_arr: List[float]

    def __init__(self, state: State, is_controllable=True, is_filter_enabled=False, noise_standard_deviation=1.0):
        self.x = state.x0
        self.y = state.y0
        self.y_prev = state.y0
        self.z = state.z0
        self.z_prev = state.z0

        self.is_controllable = is_controllable
        self.is_filter_enabled = is_filter_enabled
        self.noise_standard_deviation = noise_standard_deviation
        self.noise = self.new_noise()
        self.noise_1 = self.new_noise()

        self.a1 = state.a1
        self.a2 = state.a2
        self.a3 = state.a3
        self.a4 = state.a4
        self.a5 = state.a5
        self.a6 = state.a6

        self.t0 = state.t0
        self.u_max = state.u_max
        self.c = state.c
        self.T = state.T
        self.p = state.p

        self.x_arr = []
        self.y_arr = []
        self.z_arr = []

    def x_1(self):
        return self.x + self.t0 * (self.a1 * self.y * self.z - self.a3 * self.x)

    def y_1(self):
        return self.y + self.t0 * (self.a6 * (self.y + self.z) - self.a2 * self.x * self.z)

    def z_1(self):
        u = 0.0
        if self.is_controllable:
            u = self.u()
            print('u=', u)
        return self.z_1_0() + self.t0 * (u + self.noise_1 + self.c * self.noise)

    def z_1_0(self):
        return self.z + self.t0 * (self.a4 * self.y - self.a5 * self.z)

    def new_noise(self):
        return rand.normalvariate(self.noise_math_expectation, self.noise_standard_deviation)

    def u(self):
        tmp = -1 / self.t0 * (
                self.z_1_0() + self.p * self.y_1() + (self.T + self.c) * self.psi() + self.c * self.T * self.psi_prev())
        if tmp < 0:
            tmp = 0
        elif tmp > self.u_max:
            tmp = self.u_max
        return tmp

    def psi(self):
        return self.z + self.p * self.y

    def psi_prev(self):
        return self.z_prev + self.p * self.y_prev

    def epoch(self):
        x = self.x_1()
        y = self.y_1()
        z = self.z_1()
        self.x = x
        self.y_prev = self.y
        self.y = y
        self.z_prev = self.z
        self.z = z
        self.noise = self.noise_1
        self.noise_1 = self.new_noise()

    def train(self, epoch_count: int):
        for i in range(epoch_count):
            # print('%d) u=%e / f=%e / t0=%e / a4=%e / s=%e / a8=%e / v=%e / noise1=%e / noise=%e / c=%e' % (
            #     i, self.u(), self.f, self.t0, self.a4, self.s, self.a8, self.v, self.noise_1, self.noise, self.c))
            self.x_arr.append(self.x)
            self.y_arr.append(self.y)
            self.z_arr.append(self.z)
            if self.is_filter_enabled and i > 0:
                nw = NW(X=np.array(self.z_arr), Y=np.array(self.y_arr))
                y = nw.a_h(self.z)
                self.y = y
                self.y_arr[-1] = self.y
            try:
                self.epoch()
            except RuntimeError as ex:
                print('count of executed epoch = ', i + 1)
                print(ex)
                break


if __name__ == '__main__':
    # plt.rc('font', size=14)
    # plt.rc('axes', titlesize=14)
    # plt.ticklabel_format(axis='y', style='sci', scilimits=(-1, 1), useMathText=True, useOffset=False)

    seed = 10
    epoches = 30

    rand.seed(seed)
    eq1 = EquationSystem(state3, is_controllable=False, is_filter_enabled=False, noise_standard_deviation=0.5)
    eq1.train(epoches)

    fig = plt.figure()
    axes = Axes3D(fig)

    axes.scatter(eq1.x_arr, eq1.y_arr, eq1.z_arr)

    # plt.grid()
    # plt.tight_layout()
    plt.show()
