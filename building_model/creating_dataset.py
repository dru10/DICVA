import time
import helperfuncs
import numpy as np
import librosa
import pickle
import tensorflow as tf

seed = 42
np.random.seed(42)

DATASET_PATH = "/home/horia/dicvcaa/practic/mydataset/"
fs = 16000

audio_paths = helperfuncs.load_paths(DATASET_PATH)
audio_keys = list(audio_paths.keys())
np.random.shuffle(audio_keys)

command_mapping = {'code': 0,
                   'hello': 1,
                   'ip': 2,
                   'load': 3,
                   'news': 4,
                   'other': 5,
                   'stop': 6,
                   'terminal': 7,
                   'weather': 8,
                   'write': 9}

n_files = len(audio_keys)
n_train = round(n_files * 0.7)
n_valid = n_files - n_train

train_files = audio_keys[:n_train]
valid_files = audio_keys[n_train:]

start_valid = time.time()
valid_labels = [command_mapping[audio_paths[file]] for file in valid_files]
valid_specs = [helperfuncs.get_mel_spec_tf(helperfuncs.read_wav(path), fs) for path in valid_files]
end_valid = time.time()

print(f"Building validation = {end_valid - start_valid} (total)\nPer sample = {(end_valid - start_valid) / n_valid}")

train_labels = []
train_specs = []

start_train = time.time()
for file in train_files:
    # AUGMENTATION (waveform * 7) * 3 spectrograms

    label = command_mapping[audio_paths[file]]
    audio = helperfuncs.read_wav(file)

    helperfuncs.augment_audio(audio, fs, label, train_labels, train_specs)

    audio_n = helperfuncs.add_noise(audio)
    helperfuncs.augment_audio(audio_n, fs, label, train_labels, train_specs)

    audio_sh = helperfuncs.time_shift(audio, fs)
    helperfuncs.augment_audio(audio_sh, fs, label, train_labels, train_specs)

    audio_st = helperfuncs.time_stretch(audio, fs, "stretch")
    helperfuncs.augment_audio(audio_st, fs, label, train_labels, train_specs)

    audio_cp = helperfuncs.time_stretch(audio, fs, "compress")
    helperfuncs.augment_audio(audio_cp, fs, label, train_labels, train_specs)

    audio_pitch_minus1 = librosa.effects.pitch_shift(audio, sr=fs, n_steps=float(-1))
    helperfuncs.augment_audio(audio_pitch_minus1, fs, label, train_labels, train_specs)

    audio_pitch_plus1 = librosa.effects.pitch_shift(audio, sr=fs, n_steps=float(1))
    helperfuncs.augment_audio(audio_pitch_plus1, fs, label, train_labels, train_specs)

train_specs, train_labels = helperfuncs.shuffle_both(train_specs, train_labels)
# train_labels = tf.keras.utils.to_categorical(train_labels)
end_train = time.time()

print(f"Building train = {end_train - start_train} (total)\nPer sample = {(end_train - start_train) / n_train}")

dump_start = time.time()
with open("/home/horia/dicvcaa/practic/datasets/mfcc_64_128", 'wb') as f:
    pickle.dump((train_specs, train_labels, valid_specs, valid_labels), f)
    f.close()
dump_end = time.time()

print(f"Dumping took {dump_end - dump_start}")
