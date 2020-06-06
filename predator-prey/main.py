import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
import random as rand

x_desirable = 0
a = 3
b = 2.7
c = 2
m = 1
w1 = 1
w2 = 1
is_controllable: bool

u_min = 0
u_max = 4
u: float
uu = [0]

def equation_system(t, y):
    global u
    u = (1 / (w2 * b) - x_desirable / (y[0] * w2 * b) + a / b - y[1]) / w1 + x_desirable / (y[0] ** 2 * w2 * b) * (
            a * y[0] - b * y[0] * y[1]) - m * y[0] * y[1] + c * y[1]
    if u < 0:
        u = u_min
    elif u > u_max:
        u = u_max
    return np.array(
        [a * y[0] - b * y[0] * y[1], -c * y[1] + m * y[0] * y[1] + (u if is_controllable else 0)])


if __name__ == '__main__':
    plt.rc('font', size=14)
    plt.rc('axes', titlesize=14)
    linewidth = 2
    t0, t1 = 0, 15  # Интервал времени
    t = np.linspace(t0, t1, 1000)  # генерация точек поиска решения
    xy0 = np.array([5, 3])  # Начальное количество хищников и жертв
    y = np.zeros((len(t), len(xy0)))  # Матрица для хранения решения
    y[0, :] = xy0

    is_controllable = False
    r = integrate.ode(equation_system).set_integrator("dopri5")  # Выбор метода интегрирования
    r.set_initial_value(xy0, t0)  # Установка начальных значений
    for i in range(1, t.size):
        y[i, :] = r.integrate(t[i])  # Записываем результат интегрирования
        if not r.successful():
            raise RuntimeError("Could not integrate")

    # Без управления
    # plt.figure(1)
    # # plt.title("Без управления. График изменения численности")
    # plt.ylabel('x,y - численность')
    # plt.xlabel('t - время')
    # plt.plot(t, y, linewidth=linewidth)
    # plt.grid()
    # plt.legend(('антигены (жертвы)', 'антитела (хищники)'))
    #
    # plt.figure(2)
    # # plt.title("Без управления. Фазовый портрет")
    # plt.ylabel('y - антитела (хищники)')
    # plt.xlabel('x - антигены (жертвы)')
    # plt.plot(y[:, 0], y[:, 1], linewidth=linewidth, label='фазовая траектория')
    # plt.scatter(y[0, 0], y[0, 1], s=80, c='red', label='начальное состояние')
    # plt.grid()
    # plt.legend()

    # С управлением
    is_controllable = True
    r = integrate.ode(equation_system).set_integrator("dopri5")  # Выбор метода интегрирования
    r.set_initial_value(xy0, t0)  # Установка начальных значений
    for i in range(1, t.size):
        y[i, :] = r.integrate(t[i])  # Перезаписываем результат интегрирования
        uu.append(u)
        # if not r.successful():
        #     raise RuntimeError("Could not integrate")
    plt.figure(3)
    # plt.title("С управлением. График изменения численности")
    plt.ylabel('x,y - численность')
    plt.xlabel('t - время')
    plt.plot(t, y, linewidth=linewidth, )
    plt.grid()
    plt.legend(('антигены (жертвы)', 'антитела (хищники)'))

    plt.figure(4)
    # plt.title("С управлением. Фазовый портрет")
    plt.ylabel('y - антитела (хищники)')
    plt.xlabel('x - антигены (жертвы)')
    plt.plot(y[:, 0], y[:, 1], linewidth=linewidth, label='фазовая траектория')
    plt.scatter(y[0, 0], y[0, 1], s=80, c='red', label='начальное состояние')
    plt.grid()
    plt.legend()

    plt.figure(5)
    plt.plot(t, uu)
    plt.ylabel('u - значение управления')
    plt.xlabel('t - время')
    plt.grid()
    plt.tight_layout()

    plt.show()
