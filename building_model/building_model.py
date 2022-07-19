import time

import matplotlib.pyplot as plt
import helperfuncs
import numpy as np
import tensorflow as tf
import seaborn as sns
import librosa
import pickle

seed = 42
np.random.seed(42)

ds_type = 'mfcc_64_128'
model_name = 'mydicva_2'

start_load = time.time()
with open(f"/home/horia/dicvcaa/practic/datasets/{ds_type}", 'rb') as f:
    out = pickle.load(f)

train_specs = out[0]
train_labels = out[1]
valid_specs = out[2]
valid_labels = out[3]
end_load = time.time()
print(f"Loading data took {end_load - start_load}")

start = time.time()
train_ds = tf.data.Dataset.from_tensor_slices((train_specs, train_labels))
valid_ds = tf.data.Dataset.from_tensor_slices((valid_specs, valid_labels))

AUTOTUNE = tf.data.AUTOTUNE

batch_size = 64
train_ds = train_ds.batch(batch_size)
valid_ds = valid_ds.batch(batch_size)
train_ds = train_ds.cache().prefetch(AUTOTUNE)
valid_ds = valid_ds.cache().prefetch(AUTOTUNE)

input_shape = train_specs[0].shape
print('Input shape:', input_shape)
num_labels = 10

norm_layer = tf.keras.layers.Normalization()
norm_layer.adapt(data=train_ds.map(map_func=lambda spec, label: spec))

model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=input_shape),
    norm_layer,
    tf.keras.layers.Conv2D(64, 3, activation='relu'),
    tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(128, 3, activation='relu'),
    tf.keras.layers.Conv2D(128, 3, activation='relu', padding='same'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(num_labels, activation='softmax'),
])

model.summary()

model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    metrics=['accuracy'],
)
end = time.time()
print(f"Dataset + model definitions took {end - start}")

EPOCHS = 20
callbacks = [
    tf.keras.callbacks.EarlyStopping(verbose=1, patience=3),
    # tf.keras.callbacks.ModelCheckpoint(f'models/{ds_type}/{model_name}', verbose=1, save_best_only=True)
]
start_time = time.time()
history = model.fit(
    train_ds, 
    validation_data=valid_ds,
    epochs=EPOCHS,
    callbacks=callbacks,
)
end_time = time.time()
print(f"Training time = {end_time - start_time} seconds")

model.save(f'models/{ds_type}/{model_name}')

metrics = history.history
plt.figure()
plt.plot(history.epoch, metrics['loss'], metrics['val_loss'])
plt.legend(['loss', 'val_loss'])
plt.savefig(f"models/{ds_type}/{model_name}/loss.png")

plt.figure()
plt.plot(history.epoch, metrics['accuracy'], metrics['val_accuracy'])
plt.legend(['accuracy', 'val_accuracy'])
plt.savefig(f"models/{ds_type}/{model_name}/accuracy.png")
