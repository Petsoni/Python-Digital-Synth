import math
import random

from main import sampling_frequency


def sine_wave(frequency, n):
    """
    Returns the value of a sine wave at a given time
    :param frequency:
    :param n:
    :return:
    """
    return math.sin(2 * math.pi * frequency * n / sampling_frequency)


def sine_wave_integral(frequency, n):
    """
    Returns the integral of a sine wave at a given time
    :param frequency:
    :param n:
    :return:
    """
    return 1 - math.cos(2 * math.pi * frequency * n / sampling_frequency)


def gate_wave(frequency, n):
    """
    Returns a gate wave at a given time
    :param frequency:
    :param n:
    :return:
    """
    if frequency == 0:
        return 1
    new_n = sampling_frequency / frequency
    if n % new_n < new_n / 2:
        return 1
    return 0


def square_wave(frequency, n):
    """
    Returns a square wave at a given time
    :param frequency:
    :param n:
    :return:
    """
    if frequency == 0:
        return 1
    new_n = sampling_frequency / frequency
    if n % new_n < new_n / 2:
        return 1
    return -1


def triangular_wave(frequency, n):
    """
    Returns a triangular wave at a given time
    :param frequency:
    :param n:
    :return:
    """
    if frequency == 0:
        return 1
    new_n = sampling_frequency / frequency
    k = n % new_n
    if n % new_n < new_n / 2:
        return 1 + (k * (-2 / (new_n / 2)))
    return -1 + ((k - new_n / 2) * (2 / (new_n / 2)))


def triangular_wave_integral(frequency, n):
    """
    Returns the integral of a triangular wave at a given time
    :param frequency:
    :param n:
    :return:
    """
    if frequency == 0:
        return 0
    new_n = sampling_frequency / frequency
    k = n % new_n
    if k < new_n / 2:
        return k - k * k / (new_n / 2)
    return -(k - new_n / 2) + (k - new_n / 2) * (k - new_n / 2) / (new_n / 2)


def ramp_wave(frequency, n):
    """
    Returns a ramp wave at a given time
    :param frequency:
    :param n:
    :return:
    """
    if frequency == 0:
        return 1
    new_n = sampling_frequency / frequency
    k = n % new_n
    return 1 + (k * (-2 / new_n))


def ramp_wave_integral(frequency, n):
    """
    Returns the integral of a ramp wave at a given time
    :param frequency:
    :param n:
    :return:
    """
    if frequency == 0:
        return 1
    new_n = sampling_frequency / frequency
    k = n % new_n
    return k + k * k / new_n


def noise_wave(a1, a2):
    """
    Returns a random value between -1 and 1
    :return:
    """
    return random.random() * 2 - 1


def amplitude_modulation(f1, f2, gain, freq, time):
    """
    Returns the amplitude modulation of two frequencies at a given time
    :param f1:
    :param f2:
    :param gain:
    :param freq:
    :param time:
    :return:
    """
    return (0.5 + 0.5 * gain * f2(freq, time)) * f1(time)


def frequency_modulation(f1, f2, gain, freq, time):
    """
    Returns the frequency modulation of two frequencies at a given time
    :param f1:
    :param f2:
    :param gain:
    :param freq:
    :param time:
    :return:
    """
    if f2 == sine_wave:
        return f1(time + sampling_frequency * gain * sine_wave_integral(freq, time) / 10)
    elif f2 == square_wave:
        return f1(time + sampling_frequency * gain * triangular_wave(freq, time) / 10)
    elif f2 == triangular_wave:
        return f1(time + gain * triangular_wave_integral(freq, time) / 10)
    elif f2 == ramp_wave:
        return f1(time + gain * ramp_wave_integral(freq, time) / 10)


# Noise oscillators
oscillators = {
    'Sine Wave': sine_wave,
    'Square Wave': square_wave,
    'Triangular Wave': triangular_wave,
    'Ramp Wave': ramp_wave,
    'Noise Wave': noise_wave
}

# Modulation modes
modulation_modes = {
    'Amplitude Modulation': amplitude_modulation,
    'Frequency Modulation': frequency_modulation
}

# Modulators
modulators = {
    'Sine Wave': sine_wave,
    'Square Wave': square_wave,
    'Triangular Wave': triangular_wave,
    'Ramp Wave': ramp_wave,
}


def attack(period, n):
    """
    Returns the attack value at a given time
    :param period:
    :param n:
    :return:
    """
    v = n / period
    if v > 1:
        return 1
    return v


def decay(rate, n):
    """
    Returns the decay value at a given time
    :param rate:
    :param n:
    :return:
    """
    return math.e ** -(rate * n / sampling_frequency)


def to_pcm(value) -> bytes:
    """
    Converts a value to pcm (16-bit signed Pulse Code Modulation)
    :param value:
    :return:
    """
    if abs(value) < 0.00001:
        value = 0
    return math.floor(value * 65535 / 2).to_bytes(2, byteorder='little', signed=True)
