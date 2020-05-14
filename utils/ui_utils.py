import numpy as np
from termcolor import colored

from utils.musical_instrument import MusicalInstrument


class SheetMusic:

    def __init__(self, musical_instrument: MusicalInstrument):
        self.strings = list()
        self.musical_instrument = musical_instrument
        self.expected_note = ""

        for i in range(musical_instrument.num_strings):
            self.strings.append("----------------------------------------------------------------------")

    def display_header(self):
        header = colored("\n ********   {} PRACTICE   ********\n\n".format(self.musical_instrument.name.upper()), "yellow")
        print(header)

    def display_note(self, midi_number_to_note, max_num_frets=3):
        note = np.random.randint(0, max_num_frets)
        string = np.random.randint(0, self.musical_instrument.num_strings)
        expected_midi_number = self.musical_instrument.base_tuning[string] + note
        self.expected_note = midi_number_to_note[expected_midi_number]
        colored_notes = list()

        for i in range(self.musical_instrument.num_strings):
            if i == self.musical_instrument.num_strings - string - 1:
                self.strings[i] = "----{}{}".format(note, self.strings[i][:-5])
                colored_notes.append(colored("{}".format(note), "green", attrs=['bold']))
            else:
                self.strings[i] = "-----{}".format(self.strings[i][:-5])
                colored_notes.append(colored("-", "white"))

            colored_label = colored("{}".format(midi_number_to_note[self.musical_instrument.base_tuning[self.musical_instrument.num_strings - i - 1]]), "yellow")
            print(" {} | ----{}{}".format(colored_label, colored_notes[i], self.strings[i][5:]))

        print()



