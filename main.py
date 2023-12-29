import speech_recognition as sr
import os
import webbrowser
import openai
import datetime
import random
import numpy as np

apikey = ""

# Initialize chatStr
chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = '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'
    chatStr += f"Devesh: {query}\n Assistant: "
    
    response = openai.Completions.create(
        engine="text-davinci-003",  # engine replaces model
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    # Accessing the first completion
    completion_text = response.choices[0].text

    say(completion_text)
    chatStr += f"{completion_text}\n"
    return completion_text


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

def say(text):
    os.system(f'say "{text}"')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #print("Listening...")
        try:
            audio = r.listen(source, timeout=5)  # Adjust the timeout if needed
            #print("Audio data:", audio)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I did not get that.")
            return ""
        except sr.RequestError as e:
            print(f"Error with the speech recognition service; {e}")
            return "Some Error Occurred. Sorry from alfred"

if __name__ == '__main__':
    print("-------------------------------------")
    print("*-----  Welcome to Alfred A.I  -----*")
    print("-------------------------------------")
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        say("Good Morning Sir")
    elif 12 <= hour < 18:
        say("Good Afternoon Sir")
    elif 0 <= hour < 5 :
        say("Good evening sir")
    else:
        say("Good Evening Sir")
    say("Alfred at your service. Please tell me how may I help you?")

    while True:
        print("Listening...")
        query = takeCommand()
        # todo: Add more sites
        sites = [["youtube", "https://www.youtube.com"], ["Smash Karts", "https://smashkarts.io"], ["Zomato", "https://www.zomato.com"],["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
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

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "alfred Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)