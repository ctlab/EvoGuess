from ..plotter import *


class CasePlotter(Plotter):
    def prepare_line(self, its: List[Iteration], label: str) -> Line:
        xs, ys = [], []
        for i, it in enumerate(its):
            best = sorted(it)[0]
            ys.append(best.value)
            xs.append(i)

        return Line(xs, ys, None, label)

    def draw_line(self, ax, line: Line):
        ax.semilogy(line.xs, line.ys, lw=self.lw, label=line.label)
        if line.label is not None:
            ax.legend()

        return ax


__all__ = [
    'CasePlotter'
]
