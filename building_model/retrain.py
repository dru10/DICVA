import os

import librosa
import numpy as np
import tensorflow as tf
import helperfuncs
import matplotlib.pyplot as plt
import time

def new_model(ds_type, model_name):
    model = tf.keras.models.load_model(f"/home/horia/dicvcaa/practic/models/{ds_type}/{model_name}")
    for layer in model.layers[:-3]:
        # if layer.name not in ['dense', 'dense_1', 'dense_2']:
        layer.trainable = False

        # if layer.name == "dense_2":
    output_weights = model.layers[-1].get_weights()

    glorot = tf.initializers.GlorotUniform(seed=42)
    new_weights = tf.Variable(glorot(shape=[4096, 1], dtype=tf.float32)).numpy()
    new_bias = np.zeros(1, dtype=np.float32)
    output_weights[0] = np.concatenate((output_weights[0], new_weights), axis=1)
    output_weights[1] = np.concatenate((output_weights[1], new_bias))

    final_model = tf.keras.models.Sequential(model.layers[:-1])
    final_model.add(
        tf.keras.layers.Dense(11, activation='softmax', name='output')
    )
    final_model.layers[-1].set_weights(output_weights)

    final_model.compile(
        optimizer=tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.1),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
        metrics=['accuracy'],
    )

    final_model.summary()
    return final_model

ds_type = 'mel_64_128'
model_name = "vggish"

start = time.time()
new_model = new_model(ds_type, model_name)
end = time.time()
print(f"New model definition = {end-start}")

DATASET_PATH = "/home/horia/dicvcaa/practic/testfiles2/"
fs = 16000
command_mapping = {'code': 0,
                   'hello': 1,
                   'ip': 2,
                   'load': 3,
                   'news': 4,
                   'other': 5,
                   'stop': 6,
                   'terminal': 7,
                   'weather': 8,
                   'write': 9,
                   'test': 10}

start = time.time()
audio_paths = os.listdir(DATASET_PATH)

train_labels = []
train_specs = []
for file in audio_paths:
    # AUGMENTATION (waveform * 7) * 3 spectrograms

    label = 10
    audio = helperfuncs.read_wav(DATASET_PATH + file)

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

train_ds = tf.data.Dataset.from_tensor_slices((train_specs, train_labels))
AUTOTUNE = tf.data.AUTOTUNE

batch_size = 64
train_ds = train_ds.batch(batch_size)
train_ds = train_ds.cache().prefetch(AUTOTUNE)

EPOCHS = 8
callbacks = [
    # tf.keras.callbacks.EarlyStopping(verbose=1, patience=2),
    # tf.keras.callbacks.ModelCheckpoint(f'models/{ds_type}/{model_name}', verbose=1, save_best_only=True)
]
end = time.time()
print(f"Getting things ready = {end - start}")

start = time.time()
history = new_model.fit(
    train_ds,
    epochs=EPOCHS,
    callbacks=callbacks,
)
end = time.time()
print(f"Training took = {end - start}")

new_model.save(f'models/{ds_type}/{model_name}/retrained2/')

metrics = history.history
plt.figure()
plt.plot(history.epoch, metrics['loss'])
plt.legend(['loss'])
plt.savefig(f"models/{ds_type}/{model_name}/retrained2/loss.png")

plt.figure()
plt.plot(history.epoch, metrics['accuracy'])
plt.legend(['accuracy'])
plt.savefig(f"models/{ds_type}/{model_name}/retrained2/accuracy.png")
