import numpy as np
import math
import matplotlib.pyplot as plt
from numpy import median


class NW:
    @staticmethod
    def gauss_core(x):
        return (2 * math.pi) ** (-0.5) * math.exp(-0.5 * x ** 2)

    def __init__(self, X, Y, core=gauss_core.__func__):
        self.X = X
        self.Y = Y
        self.core = core
        self.deviation_percent = 10  # погрешность для подбора gamma в процентах (зависит от h)
        self.med_eps = 1  # медиана вариационного ряда ошибок (для gamma)
        self.h, self.gamma = self._find_h_and_gamma(1e-6, (X.max() - X.min()) / 2, (X.max() - X.min()) / X.shape[0])

    def _find_h_and_gamma(self, min_h, max_h, step_h):
        h_opt = min_h
        gamma_opt = [1] * self.X.shape[0]
        min_loo = 1e6
        arr_loo = []
        arr_h = np.arange(min_h, max_h, step_h)
        for h in arr_h:
            gamma = [1] * self.X.shape[0]
            # self.med_eps = 1
            while True:
                prev_gamma = list(gamma)
                self._calculation_gamma(gamma, h)
                a = self._loo(gamma, h)
                b = self._loo(prev_gamma, h)
                if abs(a - b) / max(a, b) * 100 <= self.deviation_percent:
                    arr_loo.append(a)
                    break
            if arr_loo[-1] < min_loo:
                min_loo = arr_loo[-1]
                h_opt = h
                gamma_opt = gamma
        # plt.figure()
        # plt.plot(arrayH, arrayLOO, linewidth=2, color='blue')
        # plt.xlabel('h')
        # plt.ylabel('LOO')
        # print("h_opt: " + str(self.h))
        # print("LOO_min: " + str(LOO_min))
        # plt.title("График зависимости LOO от h (h_opt = %f)" % self.h)
        # plt.show()
        return h_opt, gamma_opt

    def _calculation_gamma(self, gamma, h):
        alpha = []
        eps = []
        for i in range(self.X.shape[0]):
            alpha.append(
                self._a_h_for_loo(self.X[i], np.delete(self.X, [i]), np.delete(self.Y, [i]), np.delete(gamma, [i]), h,
                                  self._quartic_core))
            gamma[i] = self._quartic_core(abs(alpha[i] - self.Y[i]))
            eps.append(alpha[i] - self.Y[i])
        self.med_eps = median(eps)
        return

    def _dist(self, x1, x2):
        return abs(x1 - x2)

    def _quartic_core(self, x):
        x = x / (6 * self.med_eps)
        if abs(x) <= 1:
            return (1 - x * x) ** 2
        else:
            return 0

    def _loo(self, gamma, h):
        loo = 0
        for i in range(self.X.shape[0]):
            loo = loo + (self._a_h_for_loo(self.X[i], np.delete(self.X, [i]), np.delete(self.Y, [i]),
                                           np.delete(gamma, [i]), h, self.core) - self.Y[i]) ** 2
        return loo

    def _a_h_for_loo(self, x, X, Y, gamma, h, core):
        numerator = 0
        denominator = 0
        for i in range(X.shape[0]):
            numerator = numerator + Y[i] * gamma[i] * core(self._dist(x, X[i]) / h)
            denominator = denominator + gamma[i] * core(self._dist(x, X[i]) / h)
        if denominator == 0:
            alpha = 0
            return alpha
        else:
            alpha = numerator / denominator
            return alpha

    def a_h(self, x):
        return self._a_h_for_loo(x, self.X, self.Y, self.gamma, self.h, self.core)
