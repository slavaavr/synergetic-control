import random as rand
from typing import List
import matplotlib.pyplot as plt
from marchuk.marchuk_model_states import *
import numpy as np
from regr.nadaray_watson import NW
# from regr.lowess import NW


class EquationSystem:
    v: float
    v_prev: float  # for psi_prev function
    s: float
    f: float
    f_prev: float  # for psi_prev function
    m: float
    y1: float
    y2: float
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
    a7: float
    a8: float

    t0: float
    v_desirable: float
    u_max: float
    m_threshold: float
    c: float
    w1: float
    w2: float
    # -----------------------------
    vv: List[float]
    ff: List[float]
    uu: List[float]
    noises: List[float]
    psis: List[float]

    def __init__(self, state: State, is_controllable=True, is_filter_enabled=False, noise_standard_deviation=1.0):
        self.v = state.v0
        self.v_prev = state.v0
        self.s = state.s0
        self.f = state.f0
        self.f_prev = state.f0
        self.m = state.m0
        self.y1 = self.f
        self.y2 = self.v
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
        self.a7 = state.a7
        self.a8 = state.a8
        self.t0 = state.t0
        self.v_desirable = state.v_desirable
        self.u_max = state.u_max
        self.m_threshold = state.m_threshold
        self.c = state.c
        self.w1 = state.w1
        self.w2 = state.w2

        self.vv = []
        self.ff = []
        self.uu = []
        self.noises = []
        self.psis = []

    def v_1(self):
        return self.v + self.t0 * (self.a1 * self.v - self.a2 * self.f * self.v)

    def s_1(self):
        return self.s + self.t0 * (self.a3 * self.ksi() * self.y1 * self.y2 - self.a5 * (self.s - 1))

    def f_1(self):
        u = 0.0
        if self.is_controllable:
            u = self.u()
        return self.f + self.t0 * (
                self.a4 * (self.s - self.f) - self.a8 * self.f * self.v + u) + self.noise_1 + self.c * self.noise

    def m_1(self):
        tmp = self.m + self.t0 * (self.a6 * self.v - self.a7 * self.m)
        if tmp > 1:
            raise RuntimeError('Patient is dead m = ', tmp)
        return tmp

    def y1_1(self):
        return self.f

    def y2_1(self):
        return self.v

    def new_noise(self):
        return rand.normalvariate(self.noise_math_expectation, self.noise_standard_deviation)

    def ksi(self):
        if 0 <= self.m < self.m_threshold:
            return 1
        if self.m_threshold <= self.m <= 1:
            return (self.m - 1) / (self.m_threshold - 1)
        raise RuntimeError("Error computing ksi, m=" + str(self.m))

    def u(self):
        tmp = -1 / self.t0 * self.psi() * (
                self.w1 + 1 + self.c) - self.c * 1 / self.t0 * self.w1 * self.psi_prev() - self.a4 * (
                      self.s - self.f) + self.a8 * self.f * self.v
        if tmp < 0:
            tmp = 0
        elif tmp > self.u_max:
            tmp = self.u_max
        return tmp

    def psi(self):
        return self.f - self.fi()

    def psi_prev(self):
        return self.f_prev - self.fi_prev()

    def fi(self):
        return 1 / (self.t0 * self.a2 * self.v) * (self.w2 * (self.v - self.v_desirable) + self.v) + self.a1 / self.a2

    def fi_prev(self):
        return 1 / (self.t0 * self.a2 * self.v_prev) * (
                self.w2 * (self.v_prev - self.v_desirable) + self.v_prev) + self.a1 / self.a2

    def epoch(self):
        v = self.v_1()
        s = self.s_1()
        f = self.f_1()
        m = self.m_1()
        y1 = self.y1_1()
        y2 = self.y2_1()
        self.v_prev = self.v
        self.v = v
        self.s = s
        self.f_prev = self.f
        self.f = f
        self.m = m
        self.y1 = y1
        self.y2 = y2
        self.noise = self.noise_1
        self.noise_1 = self.new_noise()

    def train(self, epoch_count: int):
        for i in range(epoch_count):
            # print('%d) u=%e / f=%e / t0=%e / a4=%e / s=%e / a8=%e / v=%e / noise1=%e / noise=%e / c=%e' % (
            #     i, self.u(), self.f, self.t0, self.a4, self.s, self.a8, self.v, self.noise_1, self.noise, self.c))
            self.vv.append(self.v)
            self.ff.append(self.f)
            self.uu.append(self.u())
            self.noises.append(self.noise)
            self.psis.append(self.psi())
            if self.is_filter_enabled and i > 0:
                nw = NW(X=np.array(self.vv), Y=np.array(self.ff))
                f = nw.a_h(self.v)
                # print(i, '. before f=', self.f, ' after f=', f)
                self.f = f
                self.ff[-1] = self.f

            try:
                self.epoch()
            except RuntimeError as ex:
                print('count of executed epoch = ', i + 1)
                print(ex)
                break


if __name__ == '__main__':
    '''
        v - antigens
        f - antibodies
    '''
    plt.rc('font', size=14)
    plt.rc('axes', titlesize=14)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(-1, 1), useMathText=True, useOffset=False)

    seed = 10
    epoches = 15

    color = 'black'
    # color = 'dodgerblue'

    rand.seed(seed)
    eq1 = EquationSystem(fatal_state, is_controllable=False, is_filter_enabled=False, noise_standard_deviation=0.5)
    eq1.train(epoches)

    rand.seed(seed)
    eq2 = EquationSystem(fatal_state, is_controllable=True, is_filter_enabled=False, noise_standard_deviation=0.5)
    eq2.train(epoches)

    rand.seed(seed)
    eq3 = EquationSystem(fatal_state, is_controllable=True, is_filter_enabled=True, noise_standard_deviation=0.5)
    eq3.train(epoches)

    # ax.set_ylabel('V[k]', rotation='horizontal', Y=1.0)
    # ax.set_xlabel('F[k]', X=1.0)
    # ax.plot(eq2.ff, eq2.vv, linewidth=3, c='red', label='С управлением, без шума')
    # ax.plot(eq3.ff, eq3.vv, linewidth=3, c='green', label='С управлением, с шумом')
    # ax.plot(eq4.ff, eq4.vv, linewidth=3, c='blue', label='С управлением, с шумом, с фильтром')
    # ax.scatter(f0, v0, c='black', s=90, label='Начало')
    # ax.scatter(range(len(eq2.vv)), eq2.vv, c='red', label='with control')
    # ax.scatter(range(len(eq3.vv)), eq3.vv, c=color,  label='with control+filter')
    # ax.plot(eq1.vv, c='green', label='without control')

    plt.ylabel('V[k]', rotation='horizontal', Y=1.0)
    plt.xlabel('k,days', X=1.0)
    plt.plot(eq1.vv, c='black', label='Без управления')
    plt.plot(eq2.vv, c='green', label='С управлением')
    plt.plot(eq3.vv, c='blue', label='С управлением, с фильтром')

    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()
