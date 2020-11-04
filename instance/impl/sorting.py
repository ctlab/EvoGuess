from ..instance import *


class BubbleVsInsert(Instance):
    tag = 'bubble_vs_insert'

    def __init__(self, size, count):
        self.type = '%dx%d' % (size, count)
        self.name = 'Instance: Bubble Vs Insert (%d, %d)' % (size, count)
        self.path = self.build_path('sorting', self.tag, '%s_%d_%d' % (self.tag, count, size))
        super().__init__(secret_key=SecretKey(1, count * size))


class BubbleVsSelection(Instance):
    tag = 'bubble_vs_selection'

    def __init__(self, size, count):
        self.type = '%dx%d' % (size, count)
        self.name = 'Instance: Bubble Vs Selection (%d, %d)' % (size, count)
        self.path = self.build_path('sorting', self.tag, '%s_%d_%d' % (self.tag, count, size))
        super().__init__(secret_key=SecretKey(1, count * size))


class BubbleVsPancake(Instance):
    tag = 'bubble_vs_pancake'

    def __init__(self, size, count):
        self.type = '%dx%d' % (size, count)
        self.name = 'Instance: Bubble Vs Pancake (%d, %d)' % (size, count)
        self.path = self.build_path('sorting', self.tag, '%s_%d_%d' % (self.tag, count, size))
        super().__init__(secret_key=SecretKey(1, count * size))


class PancakeVsSelection(Instance):
    tag = 'pancake_vs_selection'

    def __init__(self, size, count):
        self.type = '%dx%d' % (size, count)
        self.name = 'Instance: Pancake Vs Selection (%d, %d)' % (size, count)
        self.path = self.build_path('sorting', self.tag, '%s_%d_%d' % (self.tag, count, size))
        super().__init__(secret_key=SecretKey(1, count * size))


__all__ = [
    'BubbleVsInsert',
    'BubbleVsPancake',
    'BubbleVsSelection',
    'PancakeVsSelection'
]
