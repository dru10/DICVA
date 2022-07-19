import pyttsx3

engine = pyttsx3.init()     # initialize engine

# Set Rate = how fast the voice speaks
engine.setProperty('rate', 150)
# Set Voice (English)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[11].id)

# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""

    engine.say(text)
    engine.runAndWait()