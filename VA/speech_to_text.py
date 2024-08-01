import speech_recognition as sr
import text_to_speech

def speech_to_text():

    r=sr.Recognizer()

    with sr.Microphone() as source:
        audio=r.listen(source)
        try:
            voice_data=""
            voice_data=r.recognize_google(audio)
            print(voice_data)
            return voice_data
        except sr.UnknownValueError:
            print("error")
        except sr.RequestError:
            print("error")


while True:
    # text_to_speech.text_to_speech("Want to continue?")
    print(speech_to_text())
    text_to_speech.text_to_speech("Want to continue?")
    x=speech_to_text()
    if "no" in x:
        continue
    else:
        break

# speech_to_text()
