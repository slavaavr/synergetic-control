import matplotlib.pyplot as plt
import random as rand
from typing import List
from marchuk.marchuk_model_states import *


class EquationSystem:
    v: float
    s: float
    f: float
    m: float
    y1: float
    y2: float
    is_controllable: bool
    is_noise_enabled = False
    # if noise enabled
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

    def __init__(self, state: State, is_controllable=True):
        self.v = state.v0
        self.s = state.s0
        self.f = state.f0
        self.m = state.m0
        self.y1 = self.f
        self.y2 = self.v
        self.is_controllable = is_controllable

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

    def v_1(self):
        return self.v + self.t0 * (self.a1 * self.v - self.a2 * self.f * self.v)

    def s_1(self):
        return self.s + self.t0 * (self.a3 * self.ksi() * self.y1 * self.y2 - self.a5 * (self.s - 1))

    def f_1(self):
        u = 0.0
        if self.is_controllable:
            u = self.u()
        res = self.f + self.t0 * (self.a4 * (self.s - self.f) - self.a8 * self.f * self.v + u)
        if self.is_noise_enabled:
            res += self.noise_1 + self.c * self.noise
        return res

    def m_1(self):
        tmp = self.m + self.t0 * (self.a6 * self.v - self.a7 * self.m)
        if tmp > 1:
            raise RuntimeError('Patient is dead m = ', tmp)
        return tmp

    def y1_1(self):
        return self.f

    def y2_1(self):
        return self.v

    def epoch(self):
        v = self.v_1()
        s = self.s_1()
        f = self.f_1()
        m = self.m_1()
        y1 = self.y1_1()
        y2 = self.y2_1()
        self.v = v
        self.s = s
        self.f = f
        self.m = m
        self.y1 = y1
        self.y2 = y2
        if self.is_noise_enabled:
            self.noise = self.noise_1
            self.noise_1 = self.new_noise()

    def ksi(self):
        if 0 <= self.m < self.m_threshold:
            return 1
        if self.m_threshold <= self.m <= 1:
            return (self.m - 1) / (self.m_threshold - 1)
        raise RuntimeError("Error computing ksi, m=" + str(self.m))

    def u(self):
        tmp = 1 / self.t0 * (self.fi_1() + self.w1 * self.fi() - self.f * (self.w1 + 1)) - self.a4 * (
                self.s - self.f) + self.a8 * self.f * self.v
        if tmp < 0:
            tmp = 0
        elif tmp > self.u_max:
            tmp = self.u_max
        return tmp

    def fi(self):
        return 1 / (self.t0 * self.a2 * self.v) * (self.w2 * (self.v - self.v_desirable) + self.v) + self.a1 / self.a2

    def fi_1(self):
        return 1 / (self.t0 * self.a2 * self.v_1()) * (
                self.w2 * (self.v_1() - self.v_desirable) + self.v_1()) + self.a1 / self.a2

    def enable_noise(self, noise_standard_deviation=1.0):
        self.is_noise_enabled = True
        self.noise_standard_deviation = noise_standard_deviation
        self.noise_1 = self.new_noise()
        self.noise = self.new_noise()

    def new_noise(self):
        return rand.normalvariate(self.noise_math_expectation, self.noise_standard_deviation)

    def train(self, epoch_count: int):
        for i in range(epoch_count):
            self.vv.append(self.v)
            self.ff.append(self.f)
            self.uu.append(self.u())
            try:
                self.epoch()
            except RuntimeError as ex:
                print('count of executed epoch = ', i + 1)
                print(ex)
                break


if __name__ == '__main__':
    plt.rc('font', size=14)
    plt.rc('axes', titlesize=14)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(-1, 1), useMathText=True, useOffset=False)

    seed = 10
    epoch = 15

    rand.seed(seed)
    a = EquationSystem(sub_clinical_state, is_controllable=True)
    a.train(epoch)
    plt.ylabel('V[k]', rotation='horizontal', Y=1.0)
    plt.xlabel('k, отсчеты времени')
    plt.plot(a.vv)
    plt.grid()


    # rand.seed(555)
    # b = EquationSystem(fatal_state, is_controllable=True)
    # b.enable_noise()
    # b.train(15)
    # plt.plot(b.vv)

    plt.tight_layout()
    plt.show()
    # colors = cm.rainbow(np.linspace(0, 1, len(vv)))
    # plt.scatter(vv, ff, c=colors)
    # plt.xlabel('антигены')
    # plt.ylabel('антителла')
