# make language selection option

from gtts import gTTS
from playsound import playsound
import os

# mytext = 'Welcome to GeeksforGeeks Joe!'
# mytext='गीक्सफॉरगीक्स जो में आपका स्वागत है!'

def text_to_speech(mytext):
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("welcome.mp3")
    playsound("welcome.mp3")
    os.remove("welcome.mp3")

# text_to_speech("Hello World")