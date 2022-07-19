import speech_recognition as sr
import globals
from playsound import playsound
import voice_assistant
import numpy as np
import sounddevice as sd
import scipy.io


def continuous_rec():
    read_next_one = False
    first_rec = []
    r = sr.Recognizer()

    playsound(globals.success)
    voice_assistant.speak("I am now listening")

    while True:
        myrec = sd.rec(globals.fs, samplerate=globals.fs, channels=1, dtype='float64')
        sd.wait()

        if max(np.max(myrec), np.min(myrec)) > globals.noise_max * 2 and read_next_one is False:
            # Speech has started, read the next one just in case
            read_next_one = True
            first_rec = myrec
            continue

        if read_next_one is True:
            # Continuation of speech
            read_next_one = False
            speech_rec = np.concatenate((first_rec, myrec), axis=None)

            max_value = np.argmax(speech_rec, axis=-1)
            if max_value < globals.fs / 2:
                speech_rec = speech_rec[0: max_value + round(globals.fs / 2)]
            else:
                speech_rec = speech_rec[max_value - round(globals.fs / 2): max_value + round(globals.fs / 2)]

            playsound(globals.success)

            scaled = np.int16(speech_rec / np.max(np.abs(speech_rec)) * 32767)
            scipy.io.wavfile.write('test.wav', globals.fs, scaled.astype(np.int16))
            audio = sr.AudioFile('test.wav')
            with audio as source:
                clean_audio = r.record(source)

            try:
                print("Recognizing")
                query = r.recognize_google(clean_audio, language="en-US").lower()
                print(f"Google thinks you said '{query}'")
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))


myrec = continuous_rec()
