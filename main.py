import glob
import statistics as stat
import soundfile as sf
import numpy as np


def get_first_chanel(tab):
    if type(tab[0]) in (tuple, list, np.ndarray):
        first_chanel = [x[0] for x in tab[:]]
        return first_chanel
    else:
        return tab


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


def filter_frequencies(frequencies):
    if len(frequencies) > 0:
        frequencies.remove(max(frequencies))
    if len(frequencies) > 0:
        frequencies.remove(min(frequencies))
    return frequencies


def delete_frequencies_out_of_range(frequencies, lower_limit, upper_limit, freq_width):
    filtered_frequencies = []

    for i in range(0, len(frequencies)):
        if lower_limit < i * freq_width / len(frequencies) < upper_limit:
            filtered_frequencies.append(frequencies[i])
        else:
            filtered_frequencies.append(0)

    return filtered_frequencies


def get_frequency_for_one_block(block, lower_limit, upper_limit, freq_width):
    frequencies = abs(np.fft.fft(block))

    filtered_frequencies = delete_frequencies_out_of_range(frequencies, lower_limit, upper_limit, freq_width)

    max_arg = np.argmax(filtered_frequencies)

    return max_arg * freq_width / len(frequencies)


def get_frequency_for_blocks(blocks, lower_limit, upper_limit, freq_width):
    frequencies = []

    for block in blocks:
        frequencies.append(get_frequency_for_one_block(block, freq_width,  lower_limit, upper_limit))

    frequencies = filter_frequencies(frequencies, lower_limit, upper_limit)

    return stat.median(frequencies)


if __name__ == '__main__':
    block_size = 4096
    upper_limit = 250
    lower_limit = 70
    women_answer = 'K'
    men_answer = 'M'

    threshold = 157

    kk = km = mm = mk = 0

    for i in glob.glob("./train/*.wav"):
        correct_answer = i[-5:-4]

        sound_file, freq_width = sf.read(i)
        first_chanel_only = get_first_chanel(sound_file)

        frequencies = []
        for start_with in range(0, len(first_chanel_only), block_size):
            block = get_block(first_chanel_only, start_with, block_size)
            frequencies.append(get_frequency_for_one_block(block, lower_limit, upper_limit, freq_width))

        freq = np.median(frequencies)

        answer = get_answer(freq, threshold)

        print(freq, answer, correct_answer)

        if answer == correct_answer == women_answer:
            kk += 1
        elif answer == correct_answer == men_answer:
            mm += 1
        elif answer == women_answer:
            km += 1
        else:
            mk += 1

    print(mm, kk, km, mk)
