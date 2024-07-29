from transformers import pipeline

# Define the intents and corresponding keywords
intents = {
    "check_weather": ["weather", "forecast"],
    "set_reminder": ["remind", "reminder"],
    "play_music": ["song", "music"],
    "send_message" : ["whatsapp","message","send"],
    "read_news" : ["news"],
    "make_call" : ["call" , "phone"]
    }

# Initialize the pipeline for sentiment-analysis (which we'll use for simplicity)
nlp = pipeline("sentiment-analysis")

def classify_intent(text):
    for intent, keywords in intents.items():
        if any(keyword in text.lower() for keyword in keywords):
            return intent
    return "unknown"

def handle_intent(intent, text):
    print(text)
    if intent == "check_weather":
        return "Sure, let me check the weather for you."
    elif intent == "set_reminder":
        return "Okay, what should I remind you about?"
    elif intent == "play_music":
        return "Playing your favorite music."
    else:
        return "Sorry, I didn't understand that."
    

# Main loop to interact with the user
def main():
    print("Hello! I'm your assistant. How can I help you today?")
    while True:
        user_input = input("You:  ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Assistant: Goodbye!")
            break
        intent = classify_intent(user_input)
        response = handle_intent(intent, user_input)
        print(f"Assistant: {response}")

if __name__ == "__main__":
    main()
