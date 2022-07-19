import random
from time import sleep
import os

import sounddevice as sd
import numpy as np
from scipy import io

commands = ['hello', 'terminal', 'ip', 'news', 'weather', 'load', 'stop', 'write', 'code', 'other']
file_indexes = [len(os.listdir(f'./mydataset/{folder}')) for folder in commands]

print(file_indexes)
fs = 16000
duration = 2

how_many = int(input("How many words do you want to insert? "))

print("Get ready")
sleep(1)
print("Set")
sleep(0.5)
print("Go")
sleep(0.5)

for i in range(how_many):
    idx = random.randint(0, 9)
    print(f"{i}: Say {commands[idx]}")
    myrec = sd.rec(duration * fs, samplerate=fs, channels=1, dtype='float32', blocking=False)
    sd.wait()
    max_value = int(np.argmax(myrec, axis=0))

    if max_value < fs/2:
        myrec = myrec[0: max_value + round(fs / 2)]
    else:
        myrec = myrec[max_value - round(fs / 2): max_value + round(fs / 2)]

    io.wavfile.write(f"mydataset/{commands[idx]}/{file_indexes[idx]}.wav", fs, myrec)
    file_indexes[idx] += 1

print("Thank you <3")
