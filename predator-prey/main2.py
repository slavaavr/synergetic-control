import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
import random as rand
from typing import List

x0 = 5
y0 = 3
t0 = .01
u_max = 10
x_desirable = 0
a = 3
b = 2.7
c = 2
m = 1
w1 = .05
w2 = .1


class EquationSystem:
    x: float
    y: float
    is_controllable: bool
    # -----------------------------
    xx: List[float]
    yy: List[float]

    def __init__(self, is_controllable=True):
        self.is_controllable = is_controllable
        self.x = x0
        self.y = y0
        self.xx = []
        self.yy = []

    def x_1(self):
        return self.x + t0 * (a * self.x - b * self.x * self.y)

    def y_1(self):
        return self.y + t0 * (-c * self.y + m * self.x * self.y + self.u())

    def epoch(self):
        x = self.x_1()
        y = self.y_1()
        self.x = x
        self.y = y

    def err(self):
        return rand.normalvariate(0, 1)

    def u(self):
        if not self.is_controllable:
            return 0
        tmp = (1 / (w2 * b) - x_desirable / (self.x * w2 * b) + a / b - self.y) / w1 + x_desirable / (
                self.x ** 2 * w2 * b) * (
                      a * self.x - b * self.x * self.y) - m * self.x * self.y + c * self.y
        if tmp < 0:
            tmp = 0
        elif tmp > u_max:
            tmp = u_max
        print(tmp)
        return tmp

    def train(self, epoch_count: int):
        for i in range(epoch_count):
            self.xx.append(self.x)
            self.yy.append(self.y)
            try:
                self.epoch()
            except RuntimeError as ex:
                print('count of executed epoch = ', i + 1)
                print(ex)
                break


if __name__ == '__main__':
    es = EquationSystem(is_controllable=True)
    es.train(100)
    plt.figure(1)
    plt.title("Без управления. График изменения численности")
    plt.ylabel('Численность')
    plt.xlabel('Время')
    plt.plot(es.xx)
    plt.plot(es.yy)
    plt.grid()
    plt.legend(('Жертвы', 'Хищники'))

    plt.figure(2)
    plt.title("Без управления. Фазовый портрет")
    plt.ylabel('Хищники')
    plt.xlabel('Жертвы')
    plt.plot(es.xx, es.yy, label='Фазовая траектория')
    plt.scatter(es.xx[0], es.yy[0], c='red', label='Начальное состояние')
    plt.grid()
    plt.legend()

    # # С управлением
    # is_controllable = True
    # plt.figure(3)
    # plt.title("С управлением. График изменения численности")
    # plt.ylabel('Численность')
    # plt.xlabel('Время')
    # plt.plot(es.xx)
    # plt.plot(es.yy)
    # plt.grid()
    # plt.legend(('Жертвы', 'Хищники'))
    #
    # plt.figure(4)
    # plt.title("С управлением. Фазовый портрет")
    # plt.ylabel('Хищники')
    # plt.xlabel('Жертвы')
    # plt.plot(es.xx, es.yy, label='Фазовая траектория')
    # plt.scatter(es.xx[0], es.yy[0], c='red', label='Начальное состояние')
    # plt.grid()
    # plt.legend()

    plt.show()
