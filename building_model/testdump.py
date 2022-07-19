import numpy as np
from matplotlib import pyplot as plt

import helperfuncs
import librosa

wavefile = "/home/horia/dicvcaa/practic/mydataset/hello/37.wav"
fs = 16000

audio = helperfuncs.read_wav(wavefile)
# audio_n = helperfuncs.add_noise(audio)
# audio_sh = helperfuncs.time_shift(audio, fs)
# audio_st = helperfuncs.time_stretch(audio, fs, "stretch")
# audio_cp = helperfuncs.time_stretch(audio, fs, "compress")
# audio_pitch_minus1 = librosa.effects.pitch_shift(audio, sr=fs, n_steps=float(-1))
# audio_pitch_plus1 = librosa.effects.pitch_shift(audio, sr=fs, n_steps=float(1))

# waves = [(audio, 'normal'),
#          (audio_n, 'noise'),
#          (audio_sh, 'time shift'),
#          (audio_st, 'stretch'),
#          (audio_cp, 'compress'),
#          (audio_pitch_minus1, 'pitch down'),
#          (audio_pitch_plus1, 'pitch up')]
#
# helperfuncs.plot_waves(waves, fs)

spec = helperfuncs.get_mel_spec_tf(audio, fs)
freq_mask = helperfuncs.time_freq_mask(spec, 'freq')
time_mask = helperfuncs.time_freq_mask(spec, 'time')

plt.figure(figsize=(20,4))
plt.subplot(1,3,1)
spectrogram = np.squeeze(spec, axis=-1)
plt.imshow(spectrogram)
plt.title("Original")
plt.axis('off')
plt.subplot(1,3,2)
spectrogram = np.squeeze(freq_mask, axis=-1)
plt.imshow(spectrogram)
plt.title("Frequency mask")
plt.axis('off')
plt.subplot(1,3,3)
spectrogram = np.squeeze(time_mask, axis=-1)
plt.imshow(spectrogram)
plt.title("Time mask")
plt.axis('off')
plt.savefig("/home/horia/dicvcaa/practic/time_freq_masks.png")

#
# helperfuncs.plot_wave_spectrogram(audio, spec, fs, "hello")
