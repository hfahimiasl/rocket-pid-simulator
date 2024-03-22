import numpy as np
import matplotlib.pyplot as plt


class Plotter:
    class Item:
        def __init__(self, label, color):
            self.__label = label
            self.__color = color
            self.__data = np.array([])

        def append(self, data):
            self.__data = np.append(self.__data, data)

        @property
        def label(self):
            return self.__label

        @property
        def color(self):
            return self.__color

        @property
        def data(self):
            return self.__data

    def __init__(self, *item: Item):
        self.__item = item
        self.__sample = 0
        self.__timeline = np.array([])

    def append(self, *data):
        self.__timeline = np.append(self.__timeline, self.__sample)
        self.__sample += 1

        for i in range(len(data)):
            self.__item[i].append(data[i])

    def draw(self):
        _, axis = plt.subplots(len(self.__item), sharex=True)

        for i in range(len(axis)):
            axis[i].set(ylabel=self.__item[i].label)
            axis[i].plot(self.__timeline, self.__item[i].data, self.__item[i].color)

        plt.show()
