import numpy as np
import math
import matplotlib.pyplot as plt


class NW:
    @staticmethod
    def gauss_core(x):
        return (2 * math.pi) ** (-0.5) * math.exp(-0.5 * x ** 2)
        # return math.exp(-0.5 * x ** 2)

    def __init__(self, X, Y, core=gauss_core.__func__):
        self.X = X
        self.Y = Y
        self.core = core
        self.h = self._find_h_opt(0.000001, (X.max() - X.min()) / 2, (X.max() - X.min()) / X.shape[0])
        print(self.h)

    def get_h_opt(self):
        return self.h

    def _dist(self, x1, x2):
        return abs(x1 - x2)

    def _find_h_opt(self, min_h, max_h, step_h):
        LOO_min = 1e6
        h_opt = min_h
        arrayLOO = []
        arrayH = np.arange(min_h, max_h, step_h)
        for h in arrayH:
            LOO = self._LOO(h)
            arrayLOO.append(LOO)
            if LOO < LOO_min:
                LOO_min = LOO
                h_opt = h
        # plt.figure()
        # plt.plot(arrayH, arrayLOO, linewidth=2, color='blue')
        # plt.xlabel('h')
        # plt.ylabel('LOO')
        # plt.title("График зависимости LOO от h (h_opt = %f)" % h_opt)
        # plt.show()
        return h_opt

    def _LOO(self, h):
        LOO = 0
        for i in range(self.X.shape[0]):
            LOO += (self._a_h_for_LOO(self.X[i], np.delete(self.X, [i]), np.delete(self.Y, [i]), h) - self.Y[i]) ** 2
        return LOO

    def _a_h_for_LOO(self, x, X, Y, h):
        numerator = 0
        denominator = 0
        for i in range(X.shape[0]):
            t = self.core(self._dist(x, X[i]) / h)
            numerator += Y[i] * t
            denominator += t
        if denominator == 0:
            alpha = 0
        else:
            alpha = numerator / denominator
        return alpha

    def a_h(self, x):
        numerator = 0
        denominator = 0
        for i in range(self.X.shape[0]):
            t = self.core(self._dist(x, self.X[i]) / self.h)
            numerator += self.Y[i] * t
            denominator += t
        if denominator == 0:
            alpha = 0
        else:
            alpha = numerator / denominator
        return alpha


if __name__ == '__main__':
    x = np.arange(0, 10, 0.3)
    y = np.sin(x)
    nw = NW(x, y)
    plt.plot(x, y, c='red')
    plt.grid()
    xx = x + 0.2
    yy = []
    for i in xx:
        yy.append(nw.a_h(i))
    plt.plot(xx, yy, c='blue', linestyle='--')
    plt.show()
