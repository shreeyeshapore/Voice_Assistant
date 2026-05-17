import tkinter as tk
from PIL import Image, ImageTk
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import threading

# ---------- Voice Engine ----------
def speak(text):
    """Speak text with proper threading support"""
    try:
        output_text.set("Assistant: " + text)
        root.update()  # Update GUI immediately
        
        # Create a fresh engine for each speak call to avoid threading issues
        tts_engine = pyttsx3.init()
        tts_engine.setProperty('rate', 170)
        tts_engine.setProperty('volume', 0.9)
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        print(f"Error speaking: {e}")
        output_text.set(f"Error: Could not speak - {str(e)}")

# ---------- Speech Recognition ----------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1) 
        output_text.set("Listening...")
        root.update()
        try:
            # Waits for 5 seconds; if no sound comes, it will give an error
            audio = r.listen(source, timeout=5, phrase_time_limit=5) 
            command = r.recognize_google(audio)
            input_text.set("You: " + command)
            return command.lower()
        except Exception as e:
            print(f"Error: {e}")
            return ""

# ---------- Knowledge Base of Common Queries & Responses ----------
KNOWLEDGE_BASE = {
    # Greetings
    ("hello", "hi", "hey", "good morning", "good evening", "good afternoon"): 
        "Hello! I'm here to help. What can I do for you?",
    
    # About Assistant
    ("who are you", "what are you", "tell me about yourself"):
        "I'm your AI assistant, designed to help you with various tasks like searching the web, telling time, opening websites, and more. How can I assist you?",
    
    ("what can you do", "what are your capabilities", "what do you do"):
        "I can tell you the time, search the web, open websites like YouTube and Google, help with questions, and much more. Just ask!",
    
    # Time & Date
    ("what time", "tell me the time", "current time"):
        "TIME_SPECIAL",  # Special handler
    
    ("what date", "today's date", "tell me the date"):
        "DATE_SPECIAL",  # Special handler
    
    # Help & Support
    ("help", "can you help", "i need help"):
        "Of course! I'm here to help you. You can ask me to search the web, check the time, open websites, or just chat with me.",
    
    ("sorry", "no problem", "never mind"):
        "No worries! Always happy to help. What else can I do for you?",
    
    # Web Operations
    ("open youtube", "show youtube"):
        "YOUTUBE_OPEN",  # Special handler
    
    ("open google", "show google"):
        "GOOGLE_OPEN",  # Special handler
    
    ("search", "google search"):
        "SEARCH_SPECIAL",  # Special handler
    
    # General Conversation
    ("how are you", "how are you doing"):
        "I'm functioning perfectly, thank you for asking! How are you doing?",
    
    ("thanks", "thank you", "appreciate it"):
        "You're welcome! Happy to help. Is there anything else you'd like me to do?",
    
    ("good job", "you're awesome", "nice work"):
        "Thank you so much! I appreciate that. Let me know if you need anything else!",
    
    ("what's up", "what's new"):
        "Not much! Just here and ready to assist you with whatever you need!",
    
    # Jokes & Fun
    ("tell me a joke", "make me laugh", "joke"):
        "Why did the programmer quit his job? Because he didn't get arrays! 😄",
    
    ("make me happy", "cheer me up"):
        "Remember, every day is a new opportunity to learn something amazing! Keep smiling!",
    
    # Exit
    ("exit", "stop", "close", "quit", "goodbye", "bye", "see you"):
        "EXIT_SPECIAL",  # Special handler
    
    # Default responses for partial matches
    ("hello assistant", "hi assistant"):
        "Hey there! How can I help you today?",
}

# ---------- Function to find matching response ----------
def get_response(command):
    """Find matching response from knowledge base"""
    command_lower = command.lower().strip()
    
    # Check exact phrase matches
    for keywords, response in KNOWLEDGE_BASE.items():
        for keyword in keywords:
            if keyword in command_lower:
                return response
    
    # Default response
    return "I heard you say: '" + command + "' but I don't have a specific response for that yet. You can ask me about time, search the web, or just chat!"

# ---------- Main Logic ----------
def run_assistant():
    command = listen()

    if command == "":
        speak("I didn't hear anything. Please try again.")
        return

    # Get response from knowledge base
    response = get_response(command)
    
    # Handle special cases
    if response == "TIME_SPECIAL":
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response = f"The current time is {current_time}"
    
    elif response == "DATE_SPECIAL":
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        response = f"Today is {current_date}"
    
    elif response == "YOUTUBE_OPEN":
        response = "Opening YouTube for you."
        speak(response)
        webbrowser.open("https://www.youtube.com")
        return
    
    elif response == "GOOGLE_OPEN":
        response = "Opening Google for you."
        speak(response)
        webbrowser.open("https://www.google.com")
        return
    
    elif response == "SEARCH_SPECIAL":
        query = command.replace("search", "").replace("google", "").strip()
        if query:
            response = f"Searching Google for {query}"
            speak(response)
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return
        else:
            response = "What would you like me to search for?"
    
    elif response == "EXIT_SPECIAL":
        response = "Goodbye! Have a wonderful day!"
        speak(response)
        root.after(2000, root.destroy)
        return
    
    # Speak and display the response
    speak(response)

# ---------- Start Thread ----------
def start_assistant():
    threading.Thread(target=run_assistant).start()

# ---------- GUI ----------
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("520x620")
root.configure(bg="#0b1120")
root.resizable(True, True)
root.minsize(520, 620)

# Top banner
banner_frame = tk.Frame(root, bg="#111827")
banner_frame.pack(fill="x", padx=20, pady=(20, 10))

tk.Label(banner_frame, text="🤖 AI Assistant", font=("Segoe UI", 24, "bold"),
         bg="#111827", fg="#f8fafc").pack(pady=(18, 6))
tk.Label(banner_frame, text="Speak naturally and I will answer in voice and text.",
         font=("Segoe UI", 11), bg="#111827", fg="#94a3b8").pack(pady=(0, 18))

# Status containers
input_text = tk.StringVar()
output_text = tk.StringVar()
input_text.set("Your speech will appear here")
output_text.set("Assistant's reply will appear here")

status_frame = tk.Frame(root, bg="#0b1120")
status_frame.pack(fill="both", expand=True, padx=20)

user_card = tk.Frame(status_frame, bg="#111827", bd=0)
user_card.pack(fill="x", pady=(0, 12))

tk.Label(user_card, text="You said", font=("Segoe UI", 10, "bold"),
         bg="#111827", fg="#38bdf8").pack(anchor="w", padx=16, pady=(14, 4))
tk.Label(user_card, textvariable=input_text, font=("Segoe UI", 12),
         bg="#111827", fg="#e2e8f0", wraplength=460, justify="left").pack(fill="x", padx=16, pady=(0, 14))

assistant_card = tk.Frame(status_frame, bg="#111827", bd=0)
assistant_card.pack(fill="x", pady=(0, 12))

tk.Label(assistant_card, text="Assistant", font=("Segoe UI", 10, "bold"),
         bg="#111827", fg="#a78bfa").pack(anchor="w", padx=16, pady=(14, 4))
tk.Label(assistant_card, textvariable=output_text, font=("Segoe UI", 12),
         bg="#111827", fg="#c7d2fe", wraplength=460, justify="left").pack(fill="x", padx=16, pady=(0, 14))

# Action buttons
button_frame = tk.Frame(root, bg="#0b1120")
button_frame.pack(fill="x", padx=20, pady=(0, 14))

tk.Button(button_frame, text="🎤 Start Listening", command=start_assistant,
          bg="#8b5cf6", fg="white", activebackground="#7c3aed",
          activeforeground="white", font=("Segoe UI", 13, "bold"), bd=0,
          relief="ridge", cursor="hand2", padx=24, pady=10, width=18).pack(pady=(0, 12))

tk.Button(button_frame, text="Close", command=root.quit,
          bg="#334155", fg="white", activebackground="#475569",
          activeforeground="white", font=("Segoe UI", 11, "bold"), bd=0,
          relief="ridge", cursor="hand2", padx=20, pady=8, width=18).pack()

# Footer
footer = tk.Label(root, text="Powered by Python voice assistant", font=("Segoe UI", 9),
                  bg="#0b1120", fg="#64748b")
footer.pack(pady=(12, 20))

# Welcome the assistant at the beginning
def initial_greeting():
    speak("Hello Shreeyesha, I am your assistant. Click the purple button and speak.")

threading.Thread(target=initial_greeting).start()

root.mainloop()