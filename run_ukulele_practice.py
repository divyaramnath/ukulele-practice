import pyaudio
import os
import sys
import time

from utils.recording_utils import RecordingParams, record, get_frequency
from utils.music_utils import get_midi_number_to_note_table, get_note_to_midi_number_table, \
    convert_frequency_to_midi_number
from utils.musical_instrument import MusicalInstrument
from utils.ui_utils import SheetMusic


if __name__ == "__main__":
    os.system('cls')

    midi_number_to_note = get_midi_number_to_note_table()
    note_to_midi_number = get_note_to_midi_number_table()

    ukulele = MusicalInstrument('ukulele', 0)
    sheet_music = SheetMusic(ukulele, note_to_midi_number, midi_number_to_note)

    audio = pyaudio.PyAudio()

    recording_params = RecordingParams(format=pyaudio.paInt16,
                                       channels=1,
                                       rate=22050,
                                       input=True,
                                       frames_per_buffer=2048,
                                       time_interval=0.2)
    stream = audio.open(format=recording_params.format,
                        channels=recording_params.channels,
                        rate=recording_params.rate,
                        input=recording_params.input,
                        frames_per_buffer=recording_params.frames_per_buffer)

    while True:
        os.system('cls')
        sheet_music.display_note(midi_number_to_note)
        sleep = 10
        while sleep:
            audioVector, frames = record(stream, recording_params)
            frequency = get_frequency(audioVector, recording_params)
            midi_number = convert_frequency_to_midi_number(frequency)
            if midi_number > 108 or midi_number < 21:
                continue
            note = midi_number_to_note[midi_number]

            print("Detected note is: {}   Frequency: {:0.1f} Hz    Expected note is: {}       ".format(sleep, note, frequency, sheet_music.expected_note), end='\r')
            sleep -= 1
