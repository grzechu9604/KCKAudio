import glob

import matplotlib.pyplot as plt
import statistics as stat
import soundfile as sf


def load_sound(path):

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


def get_answer(frequency, function_threshold):
    if frequency > function_threshold:
        return 'K'
    else:
        return 'M'


def filter_frequencies(frequencies, lower_limit, upper_limit):
    frequencies = delete_frequencies_out_of_range(frequencies, lower_limit, upper_limit)
    frequencies.remove(max(frequencies))
    frequencies.remove(min(frequencies))
    return frequencies


def delete_frequencies_out_of_range(frequencies, lower_limit, upper_limit):
    filtered_frequencies = []
    for frequency in frequencies:
        if lower_limit < frequency < upper_limit:
            filtered_frequencies.append(frequency)
    return filtered_frequencies


def get_frequency_for_one_block(block):
    return 140


def get_frequency_for_blocks(blocks, lower_limit, upper_limit):
    frequencies = []
    for block in blocks:
        frequencies.append(get_frequency_for_one_block(block))

    frequencies = filter_frequencies(frequencies, lower_limit, upper_limit)

    return stat.median(frequencies)


if __name__ == '__main__':
    block_size = 2048
    upper_limit = 440
    lower_limit = 70
    women_answer = 'k'
    men_answer = 'm'

    best_threshold = 140
    threshold = 140
    threshold_change = 5
    minimal_mistake = 100000

    kk = 0
    km = 0
    mm = 0
    mk = 0

    while True:
        for i in glob.glob("./*.wav"):
            correct_answer = i[-5:-4]

            sound_file = load_sound(i)
            blocks = []
            for start_int in range (0, len(sound_file), block_size):
                blocks.append(get_block(sound_file, start_int, block_size))

            #plt.plot(block)
            #plt.show()

            freq = get_frequency_for_blocks(blocks, lower_limit, upper_limit)
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
