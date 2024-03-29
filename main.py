import speech_recognition as sr
import subprocess
import os
import webbrowser
import datetime
import random
import google.generativeai as genai
import pyautogui

apikey = genai.configure(api_key='')

# Initialize chatStr
chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    model = genai.GenerativeModel("gemini-pro")
    chatStr += f"Devesh: {query}\n Assistant: "

    response = model.generate_content(query)

    # Accessing the first completion
    completion_text = response.choices[0].text

    say(completion_text)
    chatStr += f"{completion_text}\n"
    return completion_text

def ai(prompt):
    model = genai.GenerativeModel("gemini-pro")
    text = f"Gemini Pro response for Prompt: {prompt} \n *************************\n\n"

    response = model.generate_content(prompt)

    # Handling potential missing choices
    if response.text:
        text += response.text
    else:
        text += "Gemini Pro was unable to generate any responses."

    if not os.path.exists("Gemini"):
        os.mkdir("Gemini")

    with open(
        f"Gemini/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w"
    ) as f:
        f.write(text)

def say(text):
    subprocess.run(['osascript', '-e', f'say "{text}"'])

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout=5)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I did not get that.")
            return ""
        except sr.RequestError as e:
            print(f"Error with the speech recognition service; {e}")
            return "Some Error Occurred. Sorry from Alfred"

def listen_and_type():
    r = sr.Recognizer()

    try:
        while True:
            with sr.Microphone() as source:
                print("Listening for voice typing...")
                audio = r.listen(source, timeout=None)  # Set timeout to None for continuous listening
            
            spoken_text = r.recognize_google(audio, language="en-in")
            
            #print("User said:", spoken_text)

            if "stop listening alfred" in spoken_text.lower():
                say("Stopping voice typing.")
                break

            # Type the spoken text in real-time at the current cursor position
            pyautogui.typewrite(spoken_text)
            
    except sr.UnknownValueError:
        print("Sorry, I did not hear anything.")
    except sr.RequestError as e:
        print(f"Error with the speech recognition service; {e}")
        say("Some Error Occurred. Sorry from Alfred")

def listen_for_wake_word():
    r = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            #print("Listening for wake word...")
            audio = r.listen(source)

        try:
            wake_word = r.recognize_google(audio).lower()
            if "hey alfred" in wake_word:
                print("Wake word detected!")
                say("Starting Voice Recogintion!!!")
                say("")
                hour = datetime.datetime.now().hour
                if 5 <= hour < 12:
                    say("Good Morning Sir")
                elif 12 <= hour < 18:
                    say("Good Afternoon Sir")
                elif 0 <= hour < 5:
                    say("Good evening sir")
                else:
                    say("Good Evening Sir")
                return True
        except sr.UnknownValueError:
            print("Sorry, I did not hear the wake word.")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service; {e}")

if __name__ == "__main__":
    print("-------------------------------------------------")
    print("*-----------  WELCOME TO ALFRED A.I  -----------*")
    print("-------------------------------------------------")

    listen_for_wake_word()       
    query = takeCommand()
    # todo: Add more sites
    sites = [ ["youtube", "https://www.youtube.com"],["Smash Karts", "https://smashkarts.io"],["Zomato", "https://www.zomato.com"],["wikipedia", "https://www.wikipedia.com"],["google", "https://www.google.com"]]
    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            say(f"Opening {site[0]} sir...")
            webbrowser.open(site[1])
            # todo: Add a feature to play a specific song
    if "open music" in query:
        musicPath = "/Users/deveshattri/Documents/Music.mp3"
        os.system(f"open {musicPath}")

    elif "the time" in query:
        hour = datetime.datetime.now().strftime("%H")
        min = datetime.datetime.now().strftime("%M")
        say(f"Sir time is {hour} hours and {min} minutes")

    elif "open facetime".lower() in query.lower():
        os.system(f"open /System/Applications/FaceTime.app")

    elif "open whatsapp".lower() in query.lower():
        os.system(f"open /Users/deveshattri/Desktop/WhatsApp")

    elif "start voice typing".lower() in query.lower():
        say("Starting voice typing. Speak your text. Say 'Stop listening Alfred' to stop.")
        listen_and_type()

    elif "Using artificial intelligence".lower() in query.lower():
        ai(prompt=query)
        say(
            "It's done sir. Please check the gemini folder, you will find a txt file there."
        )

    elif "alfred Quit".lower() in query.lower():
        say(
            "Thank you for using me sir, it was a great experience to work for you."
        )
        print("-------------------------------------------------")
        print("*-----  THANK YOU FOR USING ALFRED A.I!!!  -----*")
        print("-------------------------------------------------")
        exit()
        
    elif "reset chat".lower() in query.lower():
        chatStr = ""
        
    else:
        print("Chatting...")
        chat(query)