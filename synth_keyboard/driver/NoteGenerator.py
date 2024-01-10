import numpy as np
import pygame as pg

from synth_keyboard.driver.Synth import Synth


class NoteGenerator:
    def __init__(self, filename):
        self.key_list = '123456789qwertyuioasdfghjklzxcvbnm,.'
        self.notes_file = open(filename)
        self.file_contents = self.notes_file.read()
        self.notes_file.close()
        self.notes_list = self.file_contents.splitlines()

    def generate_notes(self):
        notes = {}
        freq = 16.3516  # start frequency
        pos_x, pos_y = 25, 25  # start position

        for i in range(len(self.notes_list)):
            mod = int(i / 36)
            key = self.key_list[i - mod * 36] + str(mod)
            sample = Synth().generate_wave(freq)
            color = np.array(
                [np.sin(i / 25 + 1.7) * 130 + 125, np.sin(i / 30 - 0.21) * 215 + 40, np.sin(i / 25 + 3.7) * 130 + 125])
            color = np.clip(color, 0, 255)
            notes[key] = [sample, self.notes_list[i], freq, (pos_x, pos_y), 255 * color / max(color)]
            notes[key][0].set_volume(0.11)
            notes[key][0].play()
            notes[key][0].fadeout(100)
            freq = freq * 2 ** (1 / 12)
            pos_x = pos_x + 140

            # Display the notes in a grid like fashion
            if pos_x > 1220:
                pos_x, pos_y = 25, pos_y + 56

            Synth().screen.blit(Synth().font.render(notes[key][1], 0, notes[key][4]), notes[key][3])
            pg.display.update()

        return notes
