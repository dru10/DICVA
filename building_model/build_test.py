import sounddevice as sd
import numpy as np
import scipy.io


import helperfuncs

from time import sleep

TESTFILES_PATH = "/home/horia/dicvcaa/practic/testfiles2/table/"
fs = 16000
noise_dur = 5  # seconds

myfile = helperfuncs.read_wav("/home/horia/dicvcaa/practic/mydataset/code/0.wav")

print(f"Let me calibrate\nKeep silent for {noise_dur} seconds")

noise_rec = sd.rec(noise_dur * fs, samplerate=fs, channels=1, dtype='float32')
sd.wait()
noise_rec = noise_rec[:, 0]

max_ampl = max(np.max(noise_rec), np.min(noise_rec))
print("Max amplitude", max_ampl)

if max_ampl > 0.2:
    print("Your microphone sensitivity is set too high, consider turning it down!")
    exit()

print("Calibration complete")
sleep(1)

print("Normal recording has started")

normal_dur = 1  # seconds
read_next_one = False
first_rec = []
idx = 0

while True:
    myrec = sd.rec(normal_dur * fs, samplerate=fs, channels=1, dtype='float32')
    sd.wait()

    if max(np.max(myrec), np.min(myrec)) > max_ampl * 2 and read_next_one == False:
        # Speech has started, read the next one just in case
        read_next_one = True
        first_rec = myrec
        continue

    if read_next_one == True:
        # Continuation of speech
        read_next_one = False
        speech_rec = np.concatenate((first_rec, myrec), axis=None)

        max_value = np.argmax(speech_rec, axis=-1)
        if max_value < fs / 2:
            speech_rec = speech_rec[0: max_value + round(fs / 2)]
        else:
            speech_rec = speech_rec[max_value - round(fs / 2): max_value + round(fs / 2)]

        speech_rec = helperfuncs.read_wav(speech_rec, False)
        scipy.io.wavfile.write(TESTFILES_PATH + "table" + f"_{idx}", fs, speech_rec)
        idx += 1

        print("Done")
