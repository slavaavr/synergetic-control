import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

x_desirable = 2
a = 1
b = 0.1
c = 0.4
m = 0.3
w1 = 1
w2 = 1
is_controllable: bool


def equation_system(t, y):
    u = (1 / (w2 * b) - x_desirable / (y[0] * w2 * b) + a / b - y[1]) / w1 + x_desirable / (y[0] ** 2 * w2 * b) * (
            a * y[0] - b * y[0] * y[1]) - m * y[0] * y[1] + c * y[1]
    return np.array(
        [a * y[0] - b * y[0] * y[1], -c * y[1] + m * y[0] * y[1] + (u if is_controllable else 0)])


if __name__ == '__main__':
    t0, t1 = 0, 50  # Интервал времени
    t = np.linspace(t0, t1, 100)  # генерация точек поиска решения
    xy0 = np.array([10, 10])  # Начальное количество хищников и жертв
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
    plt.figure(1)
    plt.title("Без управления. График изменения численности")
    plt.ylabel('Численность')
    plt.xlabel('Время')
    plt.plot(t, y)
    plt.grid()
    plt.legend(('Жертвы', 'Хищники'))

    plt.figure(2)
    plt.title("Без управления. Фазовый портрет")
    plt.ylabel('Хищники')
    plt.xlabel('Жертвы')
    plt.plot(y[:, 0], y[:, 1], label='Фазовая траектория')
    plt.scatter(y[0, 0], y[0, 1], c='red', label='Начальное состояние')
    plt.grid()
    plt.legend()

    # С управлением
    is_controllable = True
    r = integrate.ode(equation_system).set_integrator("dopri5")  # Выбор метода интегрирования
    r.set_initial_value(xy0, t0)  # Установка начальных значений
    for i in range(1, t.size):
        y[i, :] = r.integrate(t[i])  # Перезаписываем результат интегрирования
        if not r.successful():
            raise RuntimeError("Could not integrate")
    plt.figure(3)
    plt.title("С управлением. График изменения численности")
    plt.ylabel('Численность')
    plt.xlabel('Время')
    plt.plot(t, y)
    plt.grid()
    plt.legend(('Жертвы', 'Хищники'))

    plt.figure(4)
    plt.title("С управлением. Фазовый портрет")
    plt.ylabel('Хищники')
    plt.xlabel('Жертвы')
    plt.plot(y[:, 0], y[:, 1], label='Фазовая траектория')
    plt.scatter(y[0, 0], y[0, 1], c='red', label='Начальное состояние')
    plt.grid()
    plt.legend()

    plt.show()
