import numpy
import random
import math


class REG:
    def __init__(self, tail=40):
        self.signal = []  # массив с значениями сигнала
        self.cur_signal = 0.0  # текущее значение сигнала

        self.tail = tail  # хвост запоминания значений сигнала, влияющих на поиск окна

    def predict(self, signal):
        self.signal = signal
        self.cur_signal = signal[-1]
        # Расчет лучшего окна по текущему значению сигнала
        window = self.window()
        # Расчет предсказания следующего значения сигнала по полученному окну
        forecast = self.regression(self.signal[-window:])
        return forecast

    # Расчет лучшего окна по текущему значению сигнала
    def window(self):
        # Поиск всех окон { окно: предсказание текущего сигнала}
        windows = {}
        if len(self.signal) < 6:
            return 0
        else:
            for wind in range(2, len(self.signal[-self.tail:]) // 2):
                k = abs(self.cur_signal - self.regression(self.signal[-wind:]))
                windows[k] = wind

            return windows[min(windows.keys())]

    # функция вычисляет единственное значение
    def regression(self, signal):
        ans = 0
        yad = 0
        if len(signal) == 0:
            return 0
        for iter_s in range(len(signal)):
            k = self.kg(iter_s / len(signal))
            ans += signal[iter_s] * k

            yad += k
        ans = ans / yad
        return ans

    def kg(self, r):
        return math.exp(-0.5 * pow(r, 2))
