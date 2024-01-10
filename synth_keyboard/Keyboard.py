from synth_keyboard.driver.NoteGenerator import NoteGenerator
from synth_keyboard.driver.SoundController import SoundController
from synth_keyboard.driver.Synth import Synth


def main():
    synth = Synth()
    note_generator = NoteGenerator("extra/noteslist.txt")
    notes = note_generator.generate_notes()
    sound_controller = SoundController(notes)


if __name__ == "__main__":
    main()
