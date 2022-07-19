import librosa.effects
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd

import helperfuncs


audio_path = "/home/horia/dicvcaa/practic/mydataset/code/53f.wav"
fs = 16000

audio = helperfuncs.read_wav(audio_path)
spect = helperfuncs.get_mel_spec_tf(audio, fs)
helperfuncs.plot_wave_spectrogram(audio, spect, fs, "code")

print("Normal")
sd.play(audio, fs)
sd.wait()

audio_n = helperfuncs.add_noise(audio)
spect_n = helperfuncs.get_mel_spec_tf(audio_n, fs)
helperfuncs.plot_wave_spectrogram(audio_n, spect_n, fs, "code+noise")

print("Normal + noise")
sd.play(audio_n, fs)
sd.wait()

audio_s = helperfuncs.time_shift(audio, fs)
spect_s = helperfuncs.get_mel_spec_tf(audio_s, fs)
helperfuncs.plot_wave_spectrogram(audio_s, spect_s, fs, "code+shift")

print("Normal + timeshift")
sd.play(audio_s, fs)
sd.wait()

audio_stretch = helperfuncs.time_stretch(audio, fs, 'stretch')
spect_stretch = helperfuncs.get_mel_spec_tf(audio_stretch, fs)
helperfuncs.plot_wave_spectrogram(audio_stretch, spect_stretch, fs, "code+stretch")

print("Normal + time stretch")
sd.play(audio_stretch, fs)
sd.wait()

audio_compress = helperfuncs.time_stretch(audio, fs, 'compress')
spect_compress = helperfuncs.get_mel_spec_tf(audio_compress, fs)
helperfuncs.plot_wave_spectrogram(audio_compress, spect_compress, fs, "code+compress")

print("Normal + time compress")
sd.play(audio_compress, fs)
sd.wait()

audio_pitch_minus1 = librosa.effects.pitch_shift(audio, sr=fs, n_steps=float(-1))
spect_pitch_minus1 = helperfuncs.get_mel_spec_tf(audio_pitch_minus1, fs)
helperfuncs.plot_wave_spectrogram(audio_pitch_minus1, spect_pitch_minus1, fs, "code+pitch -1")

print("Normal + pitch -1")
sd.play(audio_pitch_minus1, fs)
sd.wait()

audio_pitch_plus1 = librosa.effects.pitch_shift(audio, sr=fs, n_steps=float(1))
spect_pitch_plus1 = helperfuncs.get_mel_spec_tf(audio_pitch_plus1, fs)
helperfuncs.plot_wave_spectrogram(audio_pitch_plus1, spect_pitch_plus1, fs, "code+pitch +1")

print("Normal + pitch +1")
sd.play(audio_pitch_plus1, fs)
sd.wait()

freq_mask = helperfuncs.time_freq_mask(spect, "freq")
time_mask = helperfuncs.time_freq_mask(spect, "time")

plt.figure()
plt.subplot(2,1,1)
plt.imshow(freq_mask)
plt.title("Frequency mask")
plt.subplot(2,1,2)
plt.imshow(time_mask)
plt.title("Time mask")
plt.show(block=False)

plt.show()
