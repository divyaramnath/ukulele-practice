import numpy as np
import termcolor


class MusicalInstrument:

    def __init__(self, name="ukulele", tuning=0):
        self.name = name
        self.tuning = tuning  # number of half-steps from original tuning

        if self.name == "ukulele":
            self.num_strings = 4
            self.base_tuning = np.array([67, 60, 64, 69])  # ['G4', 'C4', 'E4', 'A4']
            self.num_frets = 12

        self.set_tuning(tuning)

    def set_tuning(self, tuning):
        self.base_tuning += tuning



