import numpy as np
import pygame as pg


class Synth:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((1280, 720))
        self.font = pg.font.SysFont("Impact", 48)

    def generate_wave(self, frequency, duration=1.5, sampling_rate=44100):
        frames = int(duration * sampling_rate)
        arr = np.cos(2 * np.pi * frequency * np.linspace(0, duration, frames))
        arr = arr + np.cos(4 * np.pi * frequency * np.linspace(0, duration, frames))
        arr = arr - np.cos(6 * np.pi * frequency * np.linspace(0, duration, frames))
        arr = arr / max(np.abs(arr))  # triangularish waves pt1
        sound = np.asarray([32767 * arr, 32767 * arr]).T.astype(np.int16)
        sound = pg.sndarray.make_sound(sound.copy())
        return sound
