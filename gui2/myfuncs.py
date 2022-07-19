import sounddevice as sd
import numpy as np
from playsound import playsound
import os
import pywhatkit as kit
import speech_recognition as sr
import scipy.io

import globals
import helperfuncs
import voice_assistant

CONTINUE = 0
BREAK = 1
OK = 2

def measure_noise():
    noise_rec = sd.rec(5 * globals.fs, samplerate=globals.fs, channels=1, dtype='float32')
    sd.wait()
    noise_rec = noise_rec[:, 0]

    globals.noise_max = max(np.max(noise_rec), np.min(noise_rec))

    print(f"Max noise amplitude = {globals.noise_max}")

    if globals.noise_max > 0.2:
        print("Your microphone sensitivity is set too high, consider turning it down!")


def handle_command(command):
    command_type = ''
    handler = ''
    for elem in globals.supported_commands:
        if elem['name'] == command:
            command_type = elem['type']
            handler = elem['handler']

    if command == 'stop':
        voice_assistant.speak('Goodbye')
        return BREAK

    if command_type == 'conversation':
        voice_assistant.speak(handler)
    elif command_type == 'system':
        os.system(handler)
    elif command_type == 'search':
        kit.search(handler)

    return OK


def continuous_rec():

    all_commands = []

    for elem in globals.supported_commands:
        all_commands.append(elem['name'])

    print(f"Supported commands = {all_commands}")

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
                query = r.recognize_google(clean_audio, language="en-US").lower()
                print(f"Google thinks you said '{query}'")
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                continue
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                continue

            if query not in all_commands:
                voice_assistant.speak("I don't know how to do that")
                continue
            else:
                ret = handle_command(query)

                if ret == BREAK:
                    break
