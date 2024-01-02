import Audio


def low_pass_filter(x, gain, frequency, n):
    """
    Returns the output of a low pass filter at a given time for a specific input
    :param x:
    :param gain:
    :param frequency:
    :param n:
    :return:
    """
    xn = x(n)
    return xn * (1 - gain) + gain * frequency * (xn + x(n - 1)) - (2 * frequency - 1) * Audio.y_prev[0]


def high_pass_filter(x, gain, frequency, n):
    """
    Returns the output of a high pass filter at a given time for a specific input
    :param x:
    :param gain:
    :param frequency:
    :param n:
    :return:
    """
    xn = x(n)
    return xn * (1 - gain) + gain * (1 - frequency) * (xn - x(n - 1)) + (2 * frequency - 1) * Audio.y_prev[0]





