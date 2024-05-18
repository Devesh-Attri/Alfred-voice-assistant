import speech_recognition as sr
import subprocess
import os
import os.path
import webbrowser
from webbrowser import open
import datetime
import wikipedia
from datetime import date
from dataset import dataset as dataset
# from api import apikey as apikey
import random
import google.generativeai as genai
import pyautogui
import spacy
import re
import pickle
import smtplib
import requests  # For making API requests (optional, depending on chosen services)
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# from keras.models import load_model

nlp = spacy.load("en_core_web_sm")
# chatStr = ""
# # Define the path to your trained model file
# model_path = "path_to_your_trained_model.h5"  # Update this with the actual path

# # Load the trained model
# model = load_model(model_path)

# Now you can use this model for inference
# For example, model.predict(input_data) or model.evaluate(test_data)


#NLP

# Function to preprocess the query
def preprocess_query(query):
    query = query.lower()  # Lowercase the text
    query = "".join(char for char in query if char.isalnum() or char.isspace())  # Remove punctuation
    doc = nlp(query)  # Tokenize the query
    return doc

# Function to identify questions using simple pattern matching
def is_question_simple(doc):
    for token in doc[:3]:
        if token.text in ["who", "what", "where", "when", "why", "how"]:
            return True
    if doc[0].pos_ == "VERB" and doc[0].dep_ == "ROOT":
        return True
    return False


# Function to handle questions using web search
def question_handler(query):
    global chatStr
    print(chatStr)
    chatStr += f"Devesh: {query}\n Assistant: "

    # Perform a web search and read out the first result
    search_query = f"site:wikipedia.org {query}"  # Customize the search query as needed
    webbrowser.open(f"https://www.google.com/search?q={search_query}")
    say("Searching for the answer. Please wait.")
    chatStr += "Searching for the answer. Please wait.\n"

    # Note: Depending on your system and browser, you might need to adjust the delay below
    pyautogui.sleep(5)  # Wait for the search results to load

    # Read out the first paragraph from the search results
    pyautogui.hotkey("ctrl", "a")  # Select all text on the page
    pyautogui.hotkey("ctrl", "c")  # Copy the selected text
    result_text = subprocess.check_output(["pbpaste"], universal_newlines=True)

    # Speak the result
    say(result_text)
    chatStr += f"{result_text}\n"

#EMAIL
# If modifying these scopes, delete the file token.pickle .
# if you run this for the first
# t time it will take you to gmail to choose your account
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
 
 
def authenticate_gmail():
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
 
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("Starting OAuth2 flow...")
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            print("OAuth2 flow completed.")
 
        try:
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
                print("Credentials saved to token.pickle")
        except Exception as e:
            print("Error saving credentials:", e)
    
    if creds:
        service = build('gmail', 'v1', credentials=creds)
        return service
    else:
        print("Failed to obtain credentials.")
        return None


def check_mails(service):
 
    # fetching emails of today's date
    today = (date.today())
 
    today_main = today.strftime('%Y/%m/%d')
 
    # Call the Gmail API
    results = service.users().messages().list(userId='me', labelIds=["INBOX", "UNREAD"],
                                              q="after:{0} and category:Primary".format(today_main)).execute()
    # The above code will get emails from primary
    # inbox which are unread
    messages = results.get('messages', [])
 
    if not messages:
 
        # if no new emails
        print('No messages found.')
        say('No messages found.')
    else:
        m = ""
 
        # if email found
        say("{} new emails found".format(len(messages)))
 
        say("if you want to read any particular email just type read ")
        say("and for not reading type leave ")
        for message in messages:
 
            msg = service.users().messages().get(userId='me',
                                                 id=message['id'], format='metadata').execute()
 
            for add in msg['payload']['headers']:
                if add['name'] == "From":
 
                    # fetching sender's email name
                    a = str(add['value'].split("<")[0])
                    print(a)
 
                    say("email from"+a)
                    text = input()
 
                    if text == "read":
 
                        print(msg['snippet'])
 
                        # say up the mail
                        say(msg['snippet'])
 
                    else:
                        say("email passed")


def open_in_google_maps(destination):
    """Prompts user for destination and opens it in Google Maps."""
    destination.lower()
    url = f"https://www.google.com/maps/place/{destination}"
    open(url)

def handle_navigation_request(query):
  """Processes navigation requests and opens Google Maps with the destination."""
  navigation_phrases = ["navigate me to", "take me to", "guide me the way to"]
  for phrase in navigation_phrases:
    if phrase.lower() in query.lower():
      words = query.lower().split(phrase)
      # Handle potential extra spaces (e.g., "navigate me to   grocery store")
      destination = words[1].strip()
      say(f"Here are the best ways to reach {destination} (using Google Maps):")
      open_in_google_maps(destination)
      return  # Exit the function after handling the navigation request

# Function to handle different query types
# def handle_query(query):
#     query = query.replace("Alfred", "", 1).strip()
#     doc = preprocess_query(query)

#     if is_question_simple(doc):
#         question_handler(query)  # Handle questions with web search
#     elif "send email" in query.lower():
#         # Extract recipient, subject, and body from the query
#         match = re.search(r"to (\S+) subject (.+) body (.+)", query.lower())
#         if match:
#             to_address = match.group(1)
#             subject = match.group(2)
#             body = match.group(3)
#             #send_email(to_address, subject, body)
#             say("Email sent successfully.")
#         else:
#             say("Sorry, I couldn't understand the email command. Please provide recipient, subject, and body.")
#     else:
#         # Handle non-questions (commands, web search, etc.)
#         try:
#             webbrowser.open(query)  # Attempt to open in a web browser
#         except webbrowser.Error:
#             say("I'm unable to understand your query. Could you please rephrase it or provide more context?")

#AI generation
apikey = genai.configure(api_key='AIzaSyBaltaWh-fPlHnFgXQhONHhSzYdjvrhnC8')
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
            audio = r.listen(source, timeout=None)
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

            if "stop listening" in spoken_text.lower():
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
                say("Welcome to Alfred A.I!!!")
                # say("")
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

def search_files(directory, query):
    """
    Searches for the query string in all files with supported extensions within a directory.
    Args:
    directory: The directory path to search.
    query: The string to search for in the files.
    Returns:
    A list of filenames containing the query string, or an empty list if not found.
    """
    found_files = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(".doc") or filename.lower().endswith(".docx") or filename.lower().endswith(".txt"):  # Include .docx for macOS
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as f:
                    content = f.read().lower()  # Convert content to lowercase for case-insensitive search
                    if query.lower() in content:
                        found_files.append(filename)
                        return found_files

if __name__ == "__main__":
    print("-------------------------------------------------")
    print("*-----------  WELCOME TO ALFRED A.I  -----------*")
    print("-------------------------------------------------")

    listen_for_wake_word()
    while True:
        query = takeCommand()
        # try:
        sites = [ ["youtube", "https://www.youtube.com"],["Smash Karts", "https://smashkarts.io"],["Zomato", "https://www.zomato.com"],["wikipedia", "https://www.wikipedia.com"],["google", "https://www.google.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                # todo: Add a feature to play a specific song
                continue
        if "open music".lower() in query.lower():
            musicPath = "/Users/deveshattri/Documents/Music.mp3"
            os.system(f"open {musicPath}")

        elif 'who is'.lower() in query:
            say('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            say("According to Wikipedia")
            print(results)
            say(results)

        elif "the date".lower() in query.lower():
            year= date.today().strftime("%Y")
            month= date.today().strftime("%m")
            date= date.today().strftime("%d")
            say(f"Sir today is {date}-{month}-{year}")
            continue

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir time is {hour} hours and {min} minutes")
            continue

        elif "open facetime".lower() in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")
            continue

        elif "open whatsapp".lower() in query.lower():
            os.system(f"open /Users/deveshattri/Desktop/WhatsApp")
            continue

        elif "start voice typing".lower() in query.lower():
            say("Starting voice typing. Speak your text. Say 'Stop listening' to stop.")
            listen_and_type()
            continue
        elif "open my notes".lower() in query.lower():
            os.system(f"open /System/Applications/Notes.app")
            say("Here are your notes sir.")
            continue

        elif "Using artificial intelligence".lower() in query.lower():
            ai(query)
            say(
                "It's done sir. Please check the gemini folder, you will find a txt file there."
            )
            continue

        elif "check my mails".lower() in query.lower():
            SERVICE2 = authenticate_gmail()
            check_mails(SERVICE2)
            continue

        elif "I am unable to find a file with a specific content".lower() in query.lower():
            directory = "/Users/deveshattri/Desktop/dataset/Sample_docs" 
            say("Okay sir please tell me a few lines of the content in the file?")
            query= takeCommand()
            # Search for the query
            found_files = search_files(directory, query)
            # Print results
            if found_files:
                print("Files containing the query:")
                for filename in found_files:
                    print(filename)
                    continue
            else:
                print("No files found containing the query.")
                continue
           
        elif "navigate me to" or "take me to" or "guide me the way to" in query.lower():
            handle_navigation_request(query)
            continue

        elif "alfred Quit".lower() in query.lower():
            say("Thank you for using me sir, it was a great experience to work for you.")
            print("-------------------------------------------------")
            print("*-----  THANK YOU FOR USING ALFRED A.I!!!  -----*")
            print("-------------------------------------------------")
            exit()
        
        elif "reset chat".lower() in query.lower():
            chatStr = ""
            continue
        # except sr.UnknownValueError:
        #     print("Sorry, I did not hear the anything.")