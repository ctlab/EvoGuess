from ..instance import *


class BubbleVsInsert(Instance):
    tag = 'bubble_vs_insert'

    def __init__(self, count, size):
        self.name = 'Instance: Bubble Vs Insert %dx%d' % (count, size)
        self.path = './templates/BubbleVsInsertSort/BubbleVsInsertSort_%d_%d.cnf' % (count, size)
        super().__init__(secret_key=SecretKey(1, count * size))


class BubbleVsSelection(Instance):
    tag = 'bubble_vs_selection'

    def __init__(self, count, size):
        self.name = 'Instance: Bubble Vs Selection %dx%d' % (count, size)
        self.path = './templates/BubbleVsSelectionSort/BubbleVsSelectionSort_%d_%d.cnf' % (count, size)
        super().__init__(secret_key=SecretKey(1, count * size))


class BubbleVsPancake(Instance):
    tag = 'bubble_vs_pancake'

    def __init__(self, count, size):
        self.name = 'Instance: Bubble Vs Pancake %dx%d' % (count, size)
        self.path = './templates/BubbleVsPancakeSort/BubbleVsPancakeSort_%d_%d.cnf' % (count, size)
        super().__init__(secret_key=SecretKey(1, count * size))


__all__ = [
    'BubbleVsInsert',
    'BubbleVsPancake',
    'BubbleVsSelection',
]
