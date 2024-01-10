import pygame as pg

from synth_keyboard.driver.NoteGenerator import NoteGenerator
from synth_keyboard.driver.Synth import Synth


class SoundController:
    def __init__(self, notes):
        self.running = 1
        self.mod = 1
        self.key_presses = []
        self.notes = notes
        pg.display.set_caption('Digital Synth')

        while self.running:
            for event in pg.event.get():
                self.handle_event(event)

            pg.display.update()

        pg.display.set_caption("Exporting sound sequence")
        if len(self.key_presses) > 1:
            for i in range(len(self.key_presses) - 1):
                self.key_presses[-i - 1][2] = self.key_presses[-i - 1][2] - self.key_presses[-i - 2][2]
            self.key_presses[0][2] = 0  # first at zero

            with open("note_history.txt", "w") as file:
                for i in range(len(self.key_presses)):
                    file.write(str(self.key_presses[i]) + '\n')  # separate lines for readability
            file.close()

        pg.mixer.quit()
        pg.quit()

    def handle_event(self, event):

        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            self.running = False

        if event.type == pg.KEYDOWN:
            key = str(event.unicode)

            if key in '0-=':
                self.mod = '0-='.index(str(event.unicode))
            elif key in NoteGenerator("extra/noteslist.txt").key_list:
                key = key + str(self.mod)
                self.notes[key][0].play()
                self.key_presses.append([1, self.notes[key][1], pg.time.get_ticks()])
                Synth().screen.blit(Synth().font.render(self.notes[key][1], 0, (255, 255, 255)), self.notes[key][3])

        if event.type == pg.KEYUP and str(event.unicode) != '' and str(event.unicode) in NoteGenerator(
                "extra/noteslist.txt").key_list:
            key = str(event.unicode) + str(self.mod)
            self.notes[key][0].fadeout(50)
            self.key_presses.append([0, self.notes[key][1], pg.time.get_ticks()])
            Synth().screen.blit(Synth().font.render(self.notes[key][1], 0, self.notes[key][4]), self.notes[key][3])
