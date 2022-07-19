import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_io as tfio
import cv2


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
    spectrogram = tfio.audio.spectrogram(audio_t, nfft=n_fft, window=n_fft, stride=hop_len)
    mel_spectrogram = tfio.audio.melscale(spectrogram, fs, mels=n_mels, fmin=0, fmax=8000)
    mel_spectrogram_db = tfio.audio.dbscale(mel_spectrogram, top_db=80)
    mel_spectrogram_db = tf.reverse(tf.transpose(mel_spectrogram_db), [0])

    mel_spectrogram_db = mel_spectrogram_db[..., tf.newaxis]
    return mel_spectrogram_db
