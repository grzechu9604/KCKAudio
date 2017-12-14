import glob

import matplotlib.pyplot as plt
import soundfile as sf


def load_sound_frames(path):

    data, sound_file = sf.read(path)

    return data


def get_block(tab, start_with, size):
    block_to_return = []
    for i in range(0, size):
        if len(tab) > i + start_with:
            block_to_return.append(tab[i + start_with] * (-2 / (size ** 2) * i * (i - size)))
        else:
            break
    return block_to_return


def get_answer(blocks):
    return 'K'


if __name__ == '__main__':
    best_threshold = 140
    threshold = 140
    threshold_change = 5
    women_answer = 'k'
    men_answer = 'm'
    kk = 0
    km = 0
    mm = 0
    mk = 0
    for i in glob.glob("./*.wav"):
        frames = load_sound_frames(i)
        correct_answer = i[-5:-4]
        block = get_block(frames, 0, 2048)
        plt.plot(block)
        plt.show()
        answer = get_answer(block)
        if answer == correct_answer == women_answer:
            kk += 1
        elif answer == correct_answer == men_answer:
            mm += 1
        elif answer == 'k':
            km += 1
        else:
            mk += 1

    if km > mk:
        threshold += threshold_change
    elif km < mk:
        threshold -= threshold_change

    print(threshold)
