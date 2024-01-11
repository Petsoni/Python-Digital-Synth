from synth_keyboard.driver.MusicPlayer import MusicPlayer
from synth_keyboard.driver.NoteGenerator import NoteGenerator
from synth_keyboard.driver.SoundController import SoundController
from synth_keyboard.driver.Synth import Synth


def keyboard_main():
    synth = Synth()
    note_generator = NoteGenerator("extra/noteslist.txt")
    notes = note_generator.generate_notes()
    sound_controller = SoundController(notes)


def music_player_main():
    player = MusicPlayer("extra/noteslist.txt", "extra/SuperMario.txt")
    player.play_music()
    player.save_as_wave()
    player.cleanup()


if __name__ == "__main__":
    # keyboard_main()
    music_player_main()
