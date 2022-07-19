import tensorflow as tf

ds_type = 'mel_64_128'
model_name = 'vggish'

model = tf.keras.models.load_model(f"/home/horia/dicvcaa/practic/models/{ds_type}/{model_name}")

model.summary()