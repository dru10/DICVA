import numpy as np
import tensorflow as tf
import helperfuncs
import sounddevice as sd
from time import sleep


model = tf.keras.models.load_model("/home/horia/dicvcaa/practic/models/dicva_model3")
fs = 16000
command_mapping = {0: 'code',
                   1: 'hello',
                   2: 'ip',
                   3: 'load',
                   4: 'news',
                   5: 'stop',
                   6: 'terminal',
                   7: 'weather',
                   8: 'write'}

test_file = "/home/horia/dicvcaa/practic/hello_sabin2.wav"

print("Get ready")
sleep(1)

# for i in range(10):
for i in range(1):
    # print("Say command!")
    # rec = sd.rec(1*fs, fs, 1, dtype='float32', blocking=False)
    # sd.wait()

    # wav = helperfuncs.read_wav(rec, False)
    wav = helperfuncs.read_wav(test_file)
    spec = helperfuncs.get_mel_spec_tf(wav, fs)

    spec = spec[None, :, :, :]
    prediction = model(spec)

    result = int(np.argmax(prediction))

    print(f"Predicted command: '{command_mapping[result]}' Confidence: {float(prediction[:, result])}")
    # sleep(2)
