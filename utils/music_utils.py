import numpy as np


def convert_frequency_to_midi_number(frequency):
    midi_number = 12 * np.log2(frequency / 440) + 69
    return np.round(midi_number)


def convert_midi_number_to_frequency(midi_number):
    exp = (midi_number - 69) / 12
    frequency = 440 * (2 ** exp)
    return frequency


def get_midi_number_to_note_table():
    midi_number_start = 21
    midi_number_end = 108

    notes_progression = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

    midi_number_to_note = dict()

    for i in range(midi_number_start, midi_number_end + 1):
        note = (i - midi_number_start) % 12
        octave = int((i - midi_number_start + 9) / 12)
        midi_number_to_note[i] = '{}{}'.format(notes_progression[note], octave)

    return midi_number_to_note


def get_note_to_midi_number_table():
    midi_number_start = 21
    midi_number_end = 108

    notes_progression = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

    note_to_midi_number = dict()

    for i in range(midi_number_start, midi_number_end + 1):
        note = (i - midi_number_start) % 12
        octave = int((i - midi_number_start + 9) / 12)
        note_to_midi_number[i] = '{}{}'.format(notes_progression[note], octave)

    return note_to_midi_number
