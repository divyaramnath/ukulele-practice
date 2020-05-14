import pyaudio

from utils.recording_utils import RecordingParams, record, get_frequency
from utils.music_utils import get_midi_number_to_note_table, convert_frequency_to_midi_number


if __name__ == "__main__":

    midi_number_to_note = get_midi_number_to_note_table()
    audio = pyaudio.PyAudio()

    recording_params = RecordingParams(format=pyaudio.paInt16,
                                       channels=2,
                                       rate=44100,
                                       input=True,
                                       frames_per_buffer=1024,
                                       time_interval=0.5)
    while True:
        audioVector, frames = record(audio, recording_params)
        frequency = get_frequency(audioVector, recording_params)
        midi_number = convert_frequency_to_midi_number(frequency)
        note = midi_number_to_note[midi_number]
        print("Note is: {}   Frequency: {:0.1f} Hz".format(note, frequency))
