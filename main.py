#!/usr/bin/env ipython
import glob
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np


def load_sound_frames(path):

    data, sound_file = sf.read(path)

    return data


def get_block(tab, start_with, size):
    block_to_return = []
    for i in range(0, size):
        if len(tab) > i + start_with :
            block_to_return.append(tab[i + start_with] * (1 - abs((i - size)/2 ) / size))
        else:
            break
    return block_to_return


if __name__ == '__main__':
    for i in glob.glob("./*.wav"):
        frames = load_sound_frames(i)
        correct_answer = i[-5:-4]
        block = get_block(frames, 0, 1024)
        plt.plot(block)
        plt.show()
    i = 1
