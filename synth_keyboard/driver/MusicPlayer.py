import wave

import numpy as np
import pygame as pg


class MusicPlayerSynth:
    def __init__(self, frequency, duration=1.5, sampling_rate=44100):
        self.frequency = frequency
        self.duration = duration
        self.sampling_rate = sampling_rate

    def generate_wave(self):
        frames = int(self.duration * self.sampling_rate)
        arr = np.cos(2 * np.pi * self.frequency * np.linspace(0, self.duration, frames))
        arr = np.clip(arr * 10, -1, 1)  # squarish waves
        fade = list(np.ones(frames - 4410)) + list(np.linspace(1, 0, 4410))
        arr = np.multiply(arr, np.asarray(fade))
        return list(arr)


class MusicPlayer:
    def __init__(self, notes_filename, music_filename):
        pg.init()
        pg.mixer.init()

        with open(notes_filename, "r") as file:
            notes_list = file.read().splitlines()

        freq = 16.3516  # starting frequency
        frequencies = {}

        for i in range(len(notes_list)):
            frequencies[notes_list[i]] = freq
            freq = freq * 2 ** (1 / 12)

        with open(music_filename, "r") as file:
            notes = [eval(line.rstrip()) for line in file]

        track = []
        for i in range(int(len(notes) / 2)):
            track = track + list(np.zeros(max(0, int(44.1 * (notes[i * 2][2] - 100)))))
            synth = MusicPlayerSynth(frequencies[notes[i * 2][1]], 1e-3 * (notes[i * 2 + 1][2] + 100))
            track = track + synth.generate_wave()

        arr = 32767 * np.asarray(track) * 0.5
        sound = np.asarray([arr, arr]).T.astype(np.int16)
        self.sound = pg.sndarray.make_sound(sound.copy())

    def play_music(self):
        self.sound.play()
        pg.time.wait(int(self.sound.get_length() * 1000))

    def save_as_wave(self, filename='mario.wav'):
        s_file = wave.open(filename, 'w')
        s_file.setframerate(44100)
        s_file.setnchannels(2)
        s_file.setsampwidth(2)
        s_file.writeframesraw(self.sound)
        s_file.close()

    @staticmethod
    def cleanup():
        pg.mixer.quit()
        pg.quit()
