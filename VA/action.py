import text_to_speech
import speech_to_text
import datetime
import webbrowser
import weather
import pywhatkit
import wikipedia
import pyjokes
import subprocess
import os
import torch
import matplotlib.pyplot as plt
import socket
from diffusers import StableDiffusionXLPipeline
from diffusers import (
    KDPM2AncestralDiscreteScheduler,
    AutoencoderKL
)
# import winshell

applications = {
    "text editor": "TextEdit",
    "terminal": "Terminal",
    "safari": "Safari",
    "chrome": "Google Chrome",
    "notes": "Notes",
    "calendar": "Calendar",
    "finder": "Finder",
    "messages": "Messages",
    "mail": "Mail",
    "photos": "Photos",
    "preview": "Preview",
    "itunes": "iTunes",  # For older versions of macOS
    "music": "Music",    # For newer versions of macOS
    "app store": "App Store",
    "system preferences": "System Preferences",
    "reminders": "Reminders"
}

def pages():
    try:
        text_to_speech.text_to_speech("Want to open file with ai?")
        y=speech_to_text.speech_to_text()
        print(y)
        if "yes" in y:
            content_to_add = input("What content do you want to add to the Pages document? ")
            save_as = input("What name do you want to save the file as? (e.g., my_document.pages): ")

            file_path_to_save = f'~/Desktop/{save_as}'

            applescript = f'''
        tell application "Pages"
            activate
            make new document
            tell body of document 1
                set text to "{content_to_add}"
            end tell
            save document 1 in POSIX file "{file_path_to_save}" as "Pages document"
        end tell
    '''
            subprocess.run(['osascript', '-e', applescript], shell=True)
        else :
            text_to_speech.text_to_speech("Okay, I will only open the pages")
    except:
        text_to_speech.text_to_speech("Sorry, I am unable to open the pages")

def get_ip_address():
    try:
        # Get the hostname of the local machine
        hostname = socket.gethostname()

        # Get the IP address corresponding to the hostname
        ip_address = socket.gethostbyname(hostname)
        
        return ip_address
    except Exception as e:
        return f"Error fetching IP address: {str(e)}"

def shutdown_mac():
    try:
        subprocess.run(["osascript", "-e", 'tell app "System Events" to shut down'])
        return "Shutting down your MacBook."
    except Exception as e:
        return f"Error shutting down MacBook: {str(e)}"

def get_installed_applications():
    apps = {}
    applications_dir = "/Applications"
    for app in os.listdir(applications_dir):
        if app.endswith(".app"):
            app_name = app[:-4].lower()
            apps[app_name] = os.path.join(applications_dir, app)
    return apps

def open_application(app_name):
    apps = get_installed_applications()
    print("virtualbox" in apps)
    if app_name in applications:
        app_path = applications[app_name]
        try:
            subprocess.run(["open", "-a", app_path])
            text_to_speech.text_to_speech(f"{app_name.capitalize()} is opening...")
            return f"{app_name.capitalize()} is opening..."
        except Exception as e:
            text_to_speech.text_to_speech(f"Unable to find {app_name}.")
            return f"Unable to find {app_name}."
    elif app_name in apps:
        print("2")
        app_path = apps[app_name]
        try:
            print("1")
            subprocess.run(["open", app_path])
            text_to_speech.text_to_speech(f"{app_name.capitalize()} is opening...")
            return f"{app_name.capitalize()} is opening..."
        except Exception as e:
            text_to_speech.text_to_speech(f"Unable to open {app_name}.")
            return f"Unable to open {app_name}."
    else:
        text_to_speech.text_to_speech(f"Sorry, I can't find {app_name}.")
        return f"Sorry, I can't find {app_name}."

def empty_recycle_bin():
    try:
        subprocess.run(["osascript", "-e", 'tell application "Finder" to empty the trash'])
        text_to_speech.text_to_speech("Recycle Bin Emptied")
        return "Recycle Bin Emptied"
    except Exception as e:
        text_to_speech.text_to_speech("Unable to empty the Recycle Bin.")
        return "Unable to empty the Recycle Bin."

def send_email(to,  body):
    # Properly format the subject and body for the mailto link
    # subject = subject.replace(" ", "%20")
    body = body.replace(" ", "%20").replace("\n", "%0A")
    mailto_link = f'mailto:{to}?body={body}'
    
    try:
        webbrowser.open(mailto_link)
        text_to_speech.text_to_speech("Opening default mail client to send an email")
        return "Opening default mail client to send an email"
    except Exception as e:
        text_to_speech.text_to_speech(f"Error opening email client: {str(e)}")
        return f"Error opening email client: {str(e)}"

def image(data):
    try:
        text_to_speech.text_to_speech("What type of image do you want?")
        prompt=speech_to_text.speech_to_text()
        print(prompt)
        vae=AutoencoderKL.from_pretrained(
        "madebyollin/sdxl-vae-fp16-fix",
        torch_dtype=torch.float16)
        pipe = StableDiffusionXLPipeline.from_pretrained(
            "Corcelio/mobius",
            vae=vae,
            torch_dtype=torch.float16
    )
        pipe.scheduler = KDPM2AncestralDiscreteScheduler.from_config(pipe.scheduler.config)
        pipe.to('cuda')
        image = pipe(
        prompt,
        #   negative_prompt=negative_prompt,
        width=1024,
        height=1024,
        guidance_scale=7,
        num_inference_steps=50,
        clip_skip=3
    ).images[0]

        image.save("generated_image.png")
        plt.imshow(image)
        plt.show()
    except:
        text_to_speech.text_to_speech("Unable to generate image")
        
def Action(data):
    user_data=data.lower()

    if "what is your name" in user_data.lower():
        text_to_speech.text_to_speech("My name is virtual assistant")
        return "My name is virtual assistant"
    
    elif "create image" in user_data or "generate image" in user_data:
        image(user_data)

    elif "hello" in user_data.lower() or "hi" in user_data.lower():
        text_to_speech.text_to_speech("hey, how can I help you?")
        return "hey, how can I help you?"
    
    elif "how are you" in user_data.lower():
        text_to_speech.text_to_speech("I am fine, thank you for asking.")
        return "I am fine, thank you for asking."
    
    elif "who are you" in user_data.lower() or "define yourself" in user_data.lower():
        text =  "Hello, I am an Assistant. Your Assistant. I am here to make your life easier. You can command me to perform various tasks such as asking questions or opening applications etcetera"
        text_to_speech.text_to_speech(text)
        return text

    elif "made you" in user_data.lower() or "created you" in user_data.lower():
        speak = "I was created by Nupur Gandhi."
        text_to_speech.text_to_speech(speak)
        return speak
    
    elif "who am i" in user_data.lower():
        speak = "You must probably be a human"
        text_to_speech.text_to_speech(speak)
        return speak
    
    elif "why do you exist" in user_data.lower() or "why did you come to this word" in user_data.lower():
        speak ="It is a secret"
        text_to_speech.text_to_speech(speak)
        return speak

    elif "good morning" in user_data:
        text_to_speech.text_to_speech("good morning")
        return "good morning"

    elif "time" in user_data:
        current_time=datetime.datetime.now().strftime('%I:%M%p')
        time='Current time'+current_time
        text_to_speech.text_to_speech(str(time))
        return time
    
    elif 'date' in user_data:
        date=datetime.datetime.now().strftime('%d /%m /%Y')
        text_to_speech.text_to_speech(str(date))
        return date

    elif "shutdown app" in user_data:
        text_to_speech.text_to_speech("okay")
        return "okay"
    
    elif "shutdown pc" in user_data or "shutdown my" in user_data:
        result = shutdown_mac()
        text_to_speech.text_to_speech(result)
        return result
    
    elif "play" in user_data:
        song=user_data.replace('play','')
        text_to_speech.text_to_speech("playing"+song)
        pywhatkit.playonyt(song)
        return song

    elif "open gaana" in user_data:
        webbrowser.open("https://gaana.com")
        text_to_speech.text_to_speech("gaana.com is ready for you")
        return "gaana.com is ready for you"

    elif "open youtube" in user_data:
        webbrowser.open("https://www.youtube.com")
        text_to_speech.text_to_speech("youtube is ready for you")
        return "youtube is ready for you"
    
    elif 'who is' in user_data:
        human=user_data.replace('who is',' ')
        info=wikipedia.summary(human,1)
        # print(info)
        text_to_speech.text_to_speech(info)
        return info

    elif 'where is' in user_data:
        ind=user_data.lower().split().index('is')
        location=user_data.split()[ind+1:]
        url="https://www.google.com/maps/place/" + "".join(location)
        text="This is where "+str(location)+" is."
        webbrowser.open(url)
        text_to_speech.text_to_speech(text)
        return text

    elif "search" in user_data.lower():
        ind = user_data.lower().split().index("search")
        search = user_data.split()[ind + 1:]
        webbrowser.open(
            "https://www.google.com/search?q=" + "+".join(search))
        speak ="Searching " + str(search) + " on google"
        text_to_speech.text_to_speech(speak)
        return speak

    elif "open google" in user_data:
        webbrowser.open("https://www.google.com")
        text_to_speech.text_to_speech("google is ready for you")
        return "google is ready for you"
    
    elif "google" in user_data.lower():
        ind = user_data.lower().split().index("google")
        search = user_data.split()[ind + 1:]
        webbrowser.open(
            "https://www.google.com/search?q=" + "+".join(search))
        speak ="Searching " + str(search) + " on google"
        text_to_speech.text_to_speech(speak)
        return speak
    
    elif 'joke' in user_data:
        joke = pyjokes.get_joke()
        text_to_speech.text_to_speech(joke)
        return joke

    elif "weather" in user_data:
        ans=weather.weather()
        text_to_speech.text_to_speech(ans)
        return ans
    
    elif "empty bin" in user_data or "empty recycle bin" in user_data:
        x=empty_recycle_bin()
        return x
    
    elif "open" in user_data:
        apps=get_installed_applications()
        print("photo booth" in apps)
        for app_name in applications:
            print("in for loop")
            if app_name in user_data:
                print("in if loop")
                x=open_application(app_name)
                return x
            
        for app_name in apps:
            print("in 2 for loop")
            if app_name in user_data:
                print("in 3 if loop")
                x=open_application(app_name)
                return x
            
        text_to_speech.text_to_speech("Sorry I don't know that application")
        return "Sorry I don't know that application"
    
    elif "send email to" in user_data:
        try:
            to = user_data.split("send email to")[1].strip().split()[0]
            print(to)
            # text_to_speech.text_to_speech("What is the subject?")
            # subject = speech_to_text.speech_to_text()  # Capture the user's spoken input for the subject
            # print(subject)
            text_to_speech.text_to_speech("What is the message?")
            body = speech_to_text.speech_to_text()  # Capture the user's spoken input for the email body
            print(body)
            result = send_email(to, body)
            return result
        except Exception as e:
            text_to_speech.text_to_speech("Sorry, I couldn't understand the email address, subject, or body.")
            return "Sorry, I couldn't understand the email address, subject, or body."
        
    elif "ip address" in user_data or "my ip" in user_data:
        ip_address = get_ip_address()
        text_to_speech.text_to_speech(f"Your IP address is {ip_address}")
        return f"Your IP address is {ip_address}"
    
    else:
        text_to_speech.text_to_speech("I'm not able to understand your command.")
        return "I'm not able to understand your command."