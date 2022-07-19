import os
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import helperfuncs

TESTFILES_PATH = "/home/horia/dicvcaa/practic/testfiles/"
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
fs = 16000
ds_type = 'mel_64_128'
model_name = "vggish"
model = tf.keras.models.load_model(f"/home/horia/dicvcaa/practic/models/{ds_type}/{model_name}/retrained")

test_files = os.listdir(TESTFILES_PATH)

test_audios = [helperfuncs.read_wav(TESTFILES_PATH + path) for path in test_files]
test_labels = [command_mapping[path.split('_')[0]] for path in test_files]
test_specs  = [helperfuncs.get_mel_spec_tf(audio, fs).numpy() for audio in test_audios]

test_specs = np.array(test_specs)
test_labels = np.array(test_labels)

y_pred = np.argmax(model.predict(test_specs), axis=1)
y_true = test_labels

test_acc = sum(y_pred == y_true) / len(y_true)
print(f'Test set accuracy: {test_acc:.3%}')

confusion_mtx = tf.math.confusion_matrix(y_true, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(confusion_mtx,
            xticklabels=list(command_mapping.keys()),
            yticklabels=list(command_mapping.keys()),
            annot=True, fmt='g')
plt.xlabel('Prediction')
plt.ylabel('Label')
plt.title(f"{ds_type}/{model_name}")
plt.savefig(f"models/{ds_type}/{model_name}/retrained/confusion_matrix2.png")
