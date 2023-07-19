import pyttsx3  # Library for text-to-speech conversion
import webbrowser  # Library for opening websites
import os  # Library for interacting with the operating system
import requests  # Library for making HTTP requests
import json  # Library for working with JSON data
import random  # Library for generating random values
import openai  # Library for ChatGPT integration
import speech_recognition as sr  # Library for speech recognition
1
# Initialize Text-to-Speech Engine
def speak(text):
    engine = pyttsx3.init() #  It creates an instance of the Engine class provided by pyttsx3.
    engine.say(text) # This line instructs the engine to convert the given text into speech. The say() function is used to queue the text to be spoken.
    engine.runAndWait() # This line is used to start the speech output and wait until all the text has been spoken. It blocks the program execution until the speech is complete.
#
# Initialize Speech Recognition
def get_audio():
    # Create a new instance of the Recognizer class
    r = sr.Recognizer()

    # Use the microphone as the audio source
    with sr.Microphone() as source:
        # Listen for the user's speech and capture the audio
        audio = r.listen(source)

        try:
            # Attempt to recognize the captured audio using the Google Web Speech API
            text = r.recognize_google(audio)
            # Convert the recognized text to lowercase and return it
            return text.lower()
        except sr.UnknownValueError:
            # Handle the case where the speech couldn't be recognized
            return ""
        except sr.RequestError:
            # Handle any issues with the speech recognition API
            return ""


# Open a Website
def open_website(website_name):
    standard_websites = {
        'youtube': 'https://www.youtube.com',
        'iipe': 'https://www.iipe.ac.in/',
        'facebook': 'https://www.facebook.com',
        'google': 'https://www.google.com',
        'gmail': 'https://mail.google.com',
        'chat gpt': 'https://platform.openai.com/docs/guides/chat',
        'whatsapp web': 'https://web.whatsapp.com'
    }

    if website_name in standard_websites:
        webbrowser.open(standard_websites[website_name])
        speak(f"Opening {website_name} in your web browser.")
        print(f"Opening {website_name} in your web browser.")
    else:
        speak("The website is not in the standard list. Please enter the full URL.")
        print("The website is not in the standard list. Please enter the full URL.")
        url = input("Enter the URL: ")
        webbrowser.open(url)
        speak(f"Opening the website at {url}.")
        print(f"Opening the website at {url}.")

# Play Stone Paper Scissor Game
def play_game():
    choices = ["stone", "paper", "scissor"]
    user_choice = input("Choose your move (stone/paper/scissor): ").lower()
    assistant_choice = random.choice(choices)

    speak(f"You chose {user_choice}. I chose {assistant_choice}.")
    print(f"You chose {user_choice}. I chose {assistant_choice}.")

    if user_choice == assistant_choice:
        speak("It's a tie!")
        print("It's a tie!")
    elif user_choice == "stone":
        if assistant_choice == "scissor":
            speak("You win! Stone smashes scissor.")
            print("You win! Stone smashes scissor.")
        else:
            speak("I win! Paper covers stone.")
            print("I win! Paper covers stone.")
    elif user_choice == "paper":
        if assistant_choice == "stone":
            speak("You win! Paper covers stone.")
            print("You win! Paper covers stone.")
        else:
            speak("I win! Scissor cuts paper.")
            print("I win! Scissor cuts paper.")
    elif user_choice == "scissor":
        if assistant_choice == "paper":
            speak("You win! Scissor cuts paper.")
            print("You win! Scissor cuts paper.")
        else:
            speak("I win! Stone smashes scissor.")
            print("I win! Stone smashes scissor.")
    else:
        speak("Invalid move. Please try again.")
        print("Invalid move. Please try again.")

# Open a Folder
def open_folder(folder_name):
    try:
        # Attempt to open the specified folder using the operating system's default method
        os.startfile(folder_name)
        # Speak the message indicating that the folder is being opened
        speak(f"Opening {folder_name} folder.")
        # Print the same message to the console
        print(f"Opening {folder_name} folder.")
    except:
        # Handle the case where the folder couldn't be opened
        # Speak an error message instructing the user to check the folder name
        speak("Folder not found. Please check the folder name and try again.")
        # Print the same error message to the console
        print("Folder not found. Please check the folder name and try again.")

# Get Weather Information
def get_weather(city):
    # Replace 'YOUR_WEATHER_API_KEY' with your actual weather API key
    api_key = 'YOUR_WEATHER_API_KEY'  # API key for accessing weather data

    # Set the base URL for the weather API
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # Construct the complete URL with the city and API key
    complete_url = f"{base_url}q={city}&appid={api_key}"

    # Make an HTTP GET request to the weather API
    response = requests.get(complete_url)

    # Parse the JSON response into a Python dictionary
    data = response.json()

    # Check if the 'cod' value in the response dictionary is '404'
    if data['cod'] == '404':
        # If 'cod' is '404', speak a message indicating that the city was not found
        speak("City not found. Please check the city name and try again.")
    else:
        # If 'cod' is not '404', retrieve weather information from the response
        # Extract the weather description, temperature, and humidity from the data dictionary
        weather_desc = data['weather'][0]['description']
        temp = round(data['main']['temp'] - 273.15, 2)
        humidity = data['main']['humidity']

        # Speak the weather information for the specified city
        speak(f"The weather in {city} is {weather_desc}. The temperature is {temp}°C, and the humidity is {humidity}%.")

# Get News Updates
def get_news():
    # Set your news API key
    api_key = 'YOUR_NEWS_API_KEY'

    # Define the base URL for the news API
    base_url = "http://newsapi.org/v2/top-headlines"

    # Specify the parameters for the API request
    params = {'country': 'us', 'apiKey': api_key}

    # Send a GET request to the news API with the specified parameters
    response = requests.get(base_url, params=params)

    # Parse the response as JSON data
    data = response.json()

    # Check if the status in the response is 'ok'
    if data['status'] == 'ok':
        # Retrieve the list of articles from the response
        articles = data['articles']

        # Iterate over the first 5 articles and retrieve their titles
        for idx, article in enumerate(articles[:5]):
            title = article['title']
            speak(f"News {idx + 1}: {title}")

    else:
        # If the status is not 'ok', indicate that news fetching was unsuccessful
        speak("Sorry, unable to fetch news at the moment.")

# Chat with GPT-3
def chat_with_gpt(query):
    # Set your ChatGPT API key
    api_key = 'YOUR_CHAT_GPT_API_KEY'
    openai.api_key = api_key

    try:
        # Generate a completion using the OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-002",  # Specify the engine to be used
            prompt=query,  # Set the input prompt for the model
            max_tokens=150  # Limit the response length to 150 tokens
        )

        # Extract and return the generated response
        return response['choices'][0]['text'].strip()
    except:
        # Handle any exceptions that occur during the API call
        return "Sorry, I couldn't generate a response at the moment."


# Main Function
def main():
    speak("Welcome to the Task Buddy Desktop Assistant!")
    print("Welcome to the Task Buddy Desktop Assistant!")
    speak("Which mode do you prefer? Voice or Text?")
    print("Which mode do you prefer? Voice or Text?")
    mode = input().lower()

    if 'voice' in mode:
        speak("You have selected the voice mode.")

        while True:
            speak("What can I do for you?")
            query = get_audio().lower()

            if 'open' in query:
                speak("Please enter the name of the website you want to open.")
                website_name = input().lower()
                open_website(website_name)
            elif 'folder' in query:
                speak("Please enter the folder name you want to open.")
                folder_name = input()
                open_folder(folder_name)
            elif 'weather' in query:
                speak("Please enter the city name for weather information.")
                city = input().lower()
                get_weather(city)
            elif 'news' in query:
                get_news()
            elif 'chat' in query:
                speak("Ask me anything!")
                user_query = input().lower()
                response = chat_with_gpt(user_query)
                speak(response)
            elif 'game' in query:
                speak("Let's play Stone Paper Scissor!")
                play_game()
            elif 'end' in query or 'stop' in query:
                speak("Goodbye!")
                break
            else:
                speak("Sorry, I didn't understand. Can you please repeat?")
    elif 'text' in mode:
        print("You have selected the text mode.")

        while True:
            print("What can I do for you?")
            query = input().lower()

            if 'open' in query:
                print("Please enter the name of the website you want to open.")
                website_name = input().lower()
                open_website(website_name)
            elif 'folder' in query:
                print("Please enter the folder name you want to open.")
                folder_name = input()
                open_folder(folder_name)
            elif 'weather' in query:
                print("Please enter the city name for weather information.")
                city = input().lower()
                get_weather(city)
            elif 'news' in query:
                get_news()
            elif 'chat' in query:
                print("Ask me anything!")
                user_query = input().lower()
                response = chat_with_gpt(user_query)
                print(response)
            elif 'game' in query:
                print("Let's play Stone Paper Scissor!")
                play_game()
            elif 'end' in query or 'stop' in query:
                speak("Goodbye!")
                break
            else:
                print("Sorry, I didn't understand. Can you please repeat?")
    else:
        print("Invalid mode. Please enter 'voice' or 'text'.")

if __name__ == "__main__":
    main()
