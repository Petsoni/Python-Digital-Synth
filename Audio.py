import math

import pyaudio
import Signals

time = 0
p_audio = pyaudio.PyAudio()

audio_function = lambda x: 0

y_index = 0
y_prev = [0] * 10


def callback(in_data, frame_count, time_info, flag):
    global time
    k = b''
    for i in range(frame_count):
        y = audio_function(i + time)
        y_prev.insert(0, y)
        y_prev.pop()
        k += Signals.to_pcm(y)
    time += frame_count
    return k, pyaudio.paContinue


stream = p_audio.open(format=p_audio.get_format_from_width(2),
                      channels=1,
                      rate=Signals.sampling_frequency,
                      output=True,
                      stream_callback=callback)


def start():
    stream.start_stream()


def stop():
    stream.stop_stream()
    stream.close()


def terminate():
    p_audio.terminate()
