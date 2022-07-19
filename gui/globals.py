import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

noise_max = 0
fs = 16000
model = tf.keras.models.load_model("/home/horia/dicvcaa/practic/models/mel_64_128/vggish")
command_mapping = {0: 'code',
                   1: 'hello',
                   2: 'ip',
                   3: 'load',
                   4: 'news',
                   5: 'other',
                   6: 'stop',
                   7: 'terminal',
                   8: 'weather',
                   9: 'write'}
success = "/home/horia/dicvcaa/practic/audios/process_complete.wav"
predicted_command = "None"
confidence_level = "0.000"
username = "user"