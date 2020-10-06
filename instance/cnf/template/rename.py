from os import listdir, rename
from os.path import join

if __name__ == '__main__':
    dr = '.'
    for file in listdir(dr):
        if 'BubbleVsSelectionSort' in file:
            _, a, b = file.split('_')
            new_file = 'bubble_vs_selection_%s_%s' % (a, b)
            rename(join(dr, file), join(dr, new_file))
