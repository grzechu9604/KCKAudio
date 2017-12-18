import glob

import matplotlib.pyplot as plt
import statistics as stat
import soundfile as sf
import numpy as np


def get_block(tab, start_with, size):
    block_to_return = []
    for i in range(0, size):
        if len(tab) > i + start_with:
            block_to_return.append(tab[i + start_with] * (-2 / (size ** 2) * i * (i - size)))
        else:
            break
    return block_to_return


def get_answer(frequency, function_threshold):
    if frequency > function_threshold:
        return 'K'
    else:
        return 'M'


def filter_frequencies(frequencies, lower_limit, upper_limit):
    frequencies = delete_frequencies_out_of_range(frequencies, lower_limit, upper_limit)
    if len(frequencies) > 0:
        frequencies.remove(max(frequencies))
    if len(frequencies) > 0:
        frequencies.remove(min(frequencies))
    return frequencies


def delete_frequencies_out_of_range(frequencies, lower_limit, upper_limit):
    filtered_frequencies = []
    for frequency in frequencies:
        if lower_limit < frequency < upper_limit:
            filtered_frequencies.append(frequency)
    return filtered_frequencies


def get_frequency_for_one_block(block, freq_width):
    freqencies = abs(np.fft.rfft(block))

    i = np.argmax(freqencies)

    freq = max(abs(freqencies))
    return 140


def get_frequency_for_blocks(blocks, lower_limit, upper_limit, freq_width):
    frequencies = []

    for block in blocks:
        frequencies.append(get_frequency_for_one_block(block, freq_width))

    frequencies = filter_frequencies(frequencies, lower_limit, upper_limit)

    return stat.median(frequencies)


if __name__ == '__main__':
    block_size = 2048
    upper_limit = 440
    lower_limit = 70
    women_answer = 'k'
    men_answer = 'm'

    best_threshold = threshold = 135
    threshold_change = 5
    minimal_mistake = 100000

    while True:

        kk = km = mm = mk = 0

        for i in glob.glob("./*.wav"):
            correct_answer = i[-5:-4]

            sound_file, freq_width = sf.read(i)
            blocks = []
            for start_int in range(0, len(sound_file), block_size):
                blocks.append(get_block(sound_file, start_int, block_size))

            #plt.plot(block)
            #plt.show()

            freq = get_frequency_for_blocks(blocks, lower_limit, upper_limit, freq_width)
            answer = get_answer(freq, threshold)

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

        if minimal_mistake > km + mk:
            minimal_mistake = km + mk
        else:
            break

    print(threshold, minimal_mistake)
