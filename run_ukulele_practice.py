import pyaudio
import numpy as np
import os
from termcolor import colored
import time
import argparse

from utils.music_utils import get_midi_number_to_note_table, get_note_to_midi_number_table, \
    convert_frequency_to_midi_number, note_to_fftbin
from utils.musical_instrument import MusicalInstrument
from utils.ui_utils import SheetMusic


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tries", help="Number of tries", type=int, default=100)
    parser.add_argument("--instrument", help="Type of instrument (options: ukulele)", type=str, default="ukulele")
    parser.add_argument("--speed", help="Set a speed for displaying the notes", type=int, default=20)
    parser.add_argument("--tuning", help="Number of +/- half-steps", type=int, default=0)
    args = parser.parse_args()
    return args


if __name__ == "__main__":

    args = parse_arguments()

    ##############################################################################################################
    # Setting up recording params
    NOTE_MIN = 21  # A0
    NOTE_MAX = 108  # C8
    FRAME_SIZE = 2048  # Number of samples per frame
    FRAMES_PER_FFT = 16  # FFT takes average across these many frames
    SAMPLING_FREQUENCY = 22050
    SAMPLES_PER_FFT = FRAME_SIZE * FRAMES_PER_FFT  # As SAMPLES_PER_FFT goes up, the frequency step size decreases
    # (so resolution increases); however, it will incur more delay to process new sounds.
    FREQUENCY_STEP = float(SAMPLING_FREQUENCY) / SAMPLES_PER_FFT

    ##############################################################################################################

    number_of_tries = args.tries

    midi_number_to_note = get_midi_number_to_note_table()
    note_to_midi_number = get_note_to_midi_number_table()

    ukulele = MusicalInstrument('ukulele', args.tuning)
    sheet_music = SheetMusic(ukulele)

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=SAMPLING_FREQUENCY,
                        input=True,
                        frames_per_buffer=FRAME_SIZE)
    stream.start_stream()

    # Create Hanning window function
    window = 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, SAMPLES_PER_FFT, False)))

    # Allocate space to run an FFT.
    buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
    num_frames = 0
    imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN - 1, FREQUENCY_STEP))))
    imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX + 1, FREQUENCY_STEP))))

    score = 0
    for k in range(number_of_tries):
        os.system('cls')
        sheet_music.display_header()
        sheet_music.display_note(midi_number_to_note)
        speed = args.speed

        while speed:
            # Shift the buffer down and new data in
            buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
            buf[-FRAME_SIZE:] = np.fromstring(stream.read(FRAME_SIZE), np.int16)

            # Run the FFT on the windowed buffer
            fft = np.fft.rfft(buf * window)

            # Get frequency of maximum response in range
            frequency = (np.abs(fft[imin:imax]).argmax() + imin) * FREQUENCY_STEP

            # Get note number and nearest note
            n = convert_frequency_to_midi_number(frequency)
            n0 = int(round(n))

            # Console output once we have a full buffer
            num_frames += 1

            if n0 < NOTE_MIN or n0 > NOTE_MAX:
                continue

            if num_frames >= FRAMES_PER_FFT:
                note = midi_number_to_note[n0]

                score_text = colored(" Current score: {}/{}    ".format(score, k), "magenta")
                if note == sheet_music.expected_note:
                    text = colored("Correctly detected note: {}".format(note), 'green')
                    print(" {}    {}".format(text, score_text), end='\r')
                    score += 1
                    time.sleep(1)
                    break
                else:
                    text = colored(" Detected note: {}            ".format(note), 'red')
                    print(" {}    {}".format(text, score_text), end='\r')

            speed -= 1

    score_percentage = 100 * score/number_of_tries
    result_text = colored("Your score is: {}/{}    {:.2f}%".format(score, number_of_tries, score_percentage),
                          "magenta", attrs=["bold"])
    print(" {}                              ".format(result_text))
