import sounddevice as sd
import numpy as np
from playsound import playsound
import os
import pywhatkit as kit

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


def handle_command(command, confidence):
    """
    Handles command argument
    :param command: command predicted by artificial intelligence
    :param confidence: probability that predicted command is actually what the user said
    :return: CONTINUE if user needs to repeat command, BREAK if listening must be stopped, OK if command handling was executed successfully
    """

    if confidence > 0.75 and command != 'other':
        print(f"Predicted command: '{command}' Confidence: {confidence}")
    elif command == 'other' and confidence > 0.5:
        voice_assistant.speak("I don't know how to do that")
        print(f"Command not supported. ({command}: {confidence})")
    else:
        voice_assistant.speak("Can't understand you, please repeat.")
        print(f"Couldn't quite understand, please repeat ({command}: {confidence})")
        return CONTINUE

    if command == "stop":
        voice_assistant.speak("Goodbye")
        print("Listening finished")
        return BREAK
    elif command == "hello":
        voice_assistant.speak(f"Hello there {globals.username}, happy to hear from you!")
    elif command == "code":
        os.system("code")
        voice_assistant.speak("Opening coding application")
    elif command == "ip":
        kit.search("my ip")
        voice_assistant.speak("Printing public network address on the screen")
    elif command == "news":
        kit.search("news")
        voice_assistant.speak("These are today's news")
    elif command == "weather":
        kit.search("weather")
        voice_assistant.speak("Showing today's weather")
    elif command == "terminal":
        os.system("gnome-terminal")
        voice_assistant.speak("Opening new terminal window")
    elif command == "write":
        os.system("gnome-terminal -- libreoffice --writer")
        voice_assistant.speak("Opening text editor")
    elif command == "load":
        os.system("gnome-terminal -- top")
        voice_assistant.speak("These are the processes consuming resources")

    return OK


def continuous_rec():
    read_next_one = False
    first_rec = []

    playsound(globals.success)
    voice_assistant.speak("I am now listening")

    while True:
        myrec = sd.rec(globals.fs, samplerate=globals.fs, channels=1, dtype='float32')
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

            speech_rec = helperfuncs.read_wav(speech_rec, False)
            spec = helperfuncs.get_mel_spec_tf(speech_rec, globals.fs)

            spec = spec[None, :, :, :]
            prediction = globals.model(spec)

            result = int(np.argmax(prediction))

            confidence = float(prediction[:, result])
            globals.confidence_level = str(round(confidence, 4))
            command = globals.command_mapping[result]
            globals.predicted_command = command

            ret = handle_command(command, confidence)

            if ret == CONTINUE:
                continue
            elif ret == BREAK:
                break
