import numpy as np
import pyaudio
import wave
from sys import byteorder
from array import array
from scipy.fftpack import fft

class RecordingParams:
	def __init__(self, format, channels, rate, input, frames_per_buffer, time_interval):
		self.format = format
		self.channels = channels
		self.rate = rate
		self.input = input
		self.frames_per_buffer = frames_per_buffer
		self.time_interval = time_interval


def record(audio, recording_params: RecordingParams):
	stream = audio.open(format=recording_params.format,
                channels=recording_params.channels,
                rate=recording_params.rate,
                input=recording_params.input,
                frames_per_buffer=recording_params.frames_per_buffer)

	s = array('h')
	frames = []

	for i in range(0, int(recording_params.rate / recording_params.frames_per_buffer * recording_params.time_interval)):
		data = stream.read(recording_params.frames_per_buffer)
		frames.append(data)
		snd_data = array('h', data)
		if byteorder == 'big':
			snd_data.byteswap()
		s.extend(snd_data)

	return s, frames


def get_frequency(x, recording_params: RecordingParams):
	X = fft(x)
	freq = (np.abs(X)).argmax() / recording_params.time_interval + 1
	return freq