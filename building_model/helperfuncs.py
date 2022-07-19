import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_io as tfio
import cv2


def load_paths(dataset_path):
    """
    Loads all audio files from dataset_path into dictionary with the paths as the keys and the labels as the values

    :param dataset_path: path to dataset containing all audio files
    :return: dictionary containing audio paths with labels
    """
    folders = os.listdir(dataset_path)
    folders = [folder for folder in folders if folder.find('.py') == -1]

    audio_paths = {}

    for command in folders:
        wavs = os.listdir(dataset_path + command + "/")
        for wav in wavs:
            audio_path = dataset_path + command + "/" + wav
            audio_paths[audio_path] = command

    return audio_paths


def pad_trunc(audio, fs):
    """
    Pads or truncates audio binary array to length specified by fs

    :param audio: audio binary
    :param fs: length to pad/truncate to
    :return: padded/truncated audio binary array
    """
    audio_len = audio.shape[0]

    if audio_len > fs:
        # Need to truncate
        audio = audio[:fs]
    elif audio_len < fs:
        # Need to pad
        start_pad_len = int(np.floor(fs - audio_len)/2)
        end_pad_len = fs - audio_len - start_pad_len

        start_pad = np.random.uniform(-0.001, 0.001, start_pad_len)
        end_pad = np.random.uniform(-0.001, 0.001, end_pad_len)

        audio = np.concatenate([start_pad, audio, end_pad], dtype='float32')

    return audio


def read_wav(audio_path, file=True):
    """
    Reads audio file from audio_path and returns data as numpy array

    :param audio_path: path to the audio file
    :return: numpy array containing audio values
    """
    if file:
        audio_binary, fs = librosa.load(audio_path, sr=16000)
    else:
        audio_binary = audio_path
        fs = 16000

    audio_binary = pad_trunc(audio_binary, fs)

    # if not file:
    #     audio_binary = np.squeeze(audio_binary, axis=-1)

    return audio_binary


def plot_wave(audio, sr, title):
    plt.figure()
    librosa.display.waveshow(audio, sr=sr)
    plt.title(f"Waveform for {title}")
    plt.show(block=False)

def plot_waves(waves, sr):
    plt.figure(figsize=(8, 20))
    for wave in enumerate(waves):
        plt.subplot(7,1,wave[0]+1)
        librosa.display.waveshow(wave[1][0], sr=sr)
        plt.title(wave[1][1])
        plt.axis('off')
    plt.savefig("/home/horia/dicvcaa/practic/augmented_waves.png")

    plt.figure(figsize=(8, 20))
    for wave in enumerate(waves):
        plt.subplot(7, 1, wave[0] + 1)
        spectrogram = get_mel_spec_tf(wave[1][0], sr)
        spectrogram = np.squeeze(spectrogram, axis=-1)
        plt.imshow(spectrogram)
        plt.title(wave[1][1])
        plt.axis('off')
    plt.savefig("/home/horia/dicvcaa/practic/augmented_specs.png")

# def get_mel_spectrogram(audio, fs, n_mels=64, n_fft=255, hop_len=128):
#     mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=fs, n_fft=n_fft, hop_length=hop_len, n_mels=n_mels)
#     mel_spectrogram = librosa.amplitude_to_db(mel_spectrogram, ref=np.min)
#
#     # Add a `channels` dimension, so that the spectrogram can be used as image-like input data with convolution layers
#     # (which expect shape (`batch_size`, `height`, `width`, `channels`).
#     mel_spectrogram = mel_spectrogram[..., np.newaxis]
#
#     return mel_spectrogram


def get_mel_spec_tf(audio, fs, n_mels=64, n_fft=255, hop_len=125):
    """
    Computes mel spectrogram of input numpy array

    :param audio: input numpy array repsesenting audio wave
    :param fs: sampling frequency
    :param n_mels: mumber of Mel bins for vertical axis
    :param n_fft: size of FFT
    :param hop_len: size of hops between windows
    :return: 3d tensor representing output spectrogram
    """
    audio_t = tf.convert_to_tensor(audio, dtype='float32')
    spectrogram = tfio.audio.spectrogram(audio_t, nfft=n_fft, window=n_fft,
                                         stride=hop_len)
    mel_spectrogram = tfio.audio.melscale(spectrogram, fs, mels=n_mels, fmin=0, fmax=8000)
    mel_spectrogram_db = tfio.audio.dbscale(mel_spectrogram, top_db=80)

    mfcc = tf.signal.mfccs_from_log_mel_spectrograms(mel_spectrogram_db)

    # Need to flip result to be of shape (n_mels, fs/hop_len)
    result = tf.reverse(tf.transpose(mfcc), [0])

    result = result[..., tf.newaxis]
    return result


# def plot_spectrogram(audio, fs):
#     mel_spectrogram = get_mel_spectrogram(audio, fs)
#     if len(mel_spectrogram.shape) > 2:
#         assert len(mel_spectrogram.shape) == 3
#         mel_spectrogram = np.squeeze(mel_spectrogram, axis=-1)
#
#     # plt.figure()
#     librosa.display.specshow(mel_spectrogram, sr=fs, x_axis="time", y_axis="mel")
#     plt.title("Mel Spectrogram")
#     plt.colorbar(format='%+2.0f dB')
#     # plt.show(block=False)


# def get_waveform_and_label(audio_dict, path):
#     waveform = read_wav(path)
#     label = audio_dict[path]
#
#     return waveform, label


# def plot_wvndspec(audio, fs, title, colorbar=False):
#     mel_spectrogram = get_mel_spectrogram(audio, fs)
#     if len(mel_spectrogram.shape) > 2:
#         assert len(mel_spectrogram.shape) == 3
#         mel_spectrogram = np.squeeze(mel_spectrogram, axis=-1)

#     plt.figure()
#     plt.subplot(211)
#     librosa.display.waveshow(audio, sr=fs)
#     plt.title(f"Waveform for {title}")
#     plt.subplot(212)
#
#     librosa.display.specshow(mel_spectrogram, sr=fs, y_axis="mel")
#     plt.title("Mel Spectrogram")
#     if colorbar:
#         plt.colorbar(format='%+2.0f dB')
#     plt.show(block=False)
#
#
# def get_spectrogram_and_label(audio, label):
#     spectrogram = get_mel_spectrogram(audio, 16000)
#     return spectrogram, label

def plot_wave_spectrogram(wave, spectrogram, fs, title):
    plt.figure(figsize=(16,9))
    plt.subplot(1, 2, 1)
    librosa.display.waveshow(wave, sr=fs)
    # plt.title(f"Waveform for {title}")
    plt.subplot(1, 2, 2)
    spectrogram = np.squeeze(spectrogram, axis=-1)
    plt.imshow(spectrogram)
    # plt.title(f"Corresponding MFCC spectrogram")
    plt.savefig(f"/home/horia/dicvcaa/practic/sample_horizontal.png")


def add_noise(audio):
    max_ampl = max(np.max(audio), np.min(audio))
    audio_n = audio + 0.01 * max_ampl * np.random.normal(0, 1, len(audio))

    return audio_n


def time_shift(audio, fs):
    startpoint = int(np.random.uniform(-fs/5, fs/5))

    if startpoint > 0:
        audio_s = np.concatenate((audio[startpoint:], np.random.uniform(-0.001, 0.001, startpoint)), axis=-1)
    else:
        audio_s = np.concatenate((np.random.uniform(-0.001, 0.001, -startpoint), audio[:startpoint]), axis=-1)

    return audio_s


def time_stretch(audio, fs, op='stretch'):
    if op == 'stretch':
        speed_rate = np.random.uniform(1, 1.3)
    else:
        speed_rate = np.random.uniform(0.7, 1)

    new_size = int(fs * speed_rate)

    audio_speed = cv2.resize(audio, (1, new_size)).squeeze()

    audio_speed = pad_trunc(audio_speed, fs)
    return audio_speed


def time_freq_mask(spect, op, param=10):
    spect = np.squeeze(spect, axis=-1)
    spect = tf.reverse(tf.transpose(spect), [1])

    if op == "freq":
        spect = tfio.audio.freq_mask(spect, param=param)
    elif op == "time":
        spect = tfio.audio.time_mask(spect, param=param)

    spect = tf.reverse(tf.transpose(spect), [0])
    spect = spect[..., tf.newaxis]
    return spect


def augment_audio(audio, fs, label, train_labels, train_specs):
    spect = get_mel_spec_tf(audio, fs)
    train_labels.append(label)
    train_specs.append(spect)

    freq_mask = time_freq_mask(spect, "freq")
    train_labels.append(label)
    train_specs.append(freq_mask)

    time_mask = time_freq_mask(spect, "time")
    train_labels.append(label)
    train_specs.append(time_mask)


def shuffle_both(specs, labels):
    rn_state = np.random.get_state()
    np.random.shuffle(specs)
    np.random.set_state(rn_state)
    np.random.shuffle(labels)

    return specs, labels
