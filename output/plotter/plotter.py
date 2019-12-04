import matplotlib.pyplot as plt

from typing import List, Optional

from output.parser.parser import Iteration


class Line:
    def __init__(self, xs, ys, cs, label):
        self.xs = xs
        self.ys = ys
        self.cs = cs
        self.label = label


class Plotter:
    def __init__(self, **kwargs):
        self.lw = kwargs.get('lw', 2)
        self.x_label = kwargs.get('x_label', None)
        self.y_label = kwargs.get('y_label', None)

        self.lines = []

    def add_line(self, its: List[Iteration], label: Optional[str]):
        self.lines.append(self.prepare_line(its, label))

    def show(self, configuration=111):
        self.__get_figure(configuration)
        plt.show()

    def save(self, path: str, configuration=111):
        figure = self.__get_figure(configuration)
        plt.draw()
        figure.savefig(path)

    def __get_figure(self, configuration):
        figure = plt.figure()

        mod = int(configuration / 100) * (int(configuration / 10) % 10)
        axes = [None] * mod
        for i in range(len(self.lines)):
            j = (i % mod)
            if axes[j] is None:
                axes[j] = figure.add_subplot(configuration + j)
            ax = self.draw_line(axes[j], self.lines[i])

            if self.x_label is not None:
                ax.xaxis.set_label_position('bottom')
                ax.set_xlabel(self.x_label)

            if self.y_label is not None:
                ax.yaxis.set_label_position('left')
                ax.set_ylabel(self.y_label)

        return figure

    def prepare_line(self, its: List[Iteration], label: str) -> Line:
        raise NotImplementedError

    def draw_line(self, ax, line: Line):
        raise NotImplementedError


__all__ = [
    'List',
    'Line',
    'Plotter',
    'Iteration'
]
