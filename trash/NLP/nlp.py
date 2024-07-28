import spacy
from transformers import pipeline

# Load spaCy model for NER
nlp = spacy.load("en_core_web_sm")

# Load transformer model for intent recognition
intent_recognition = pipeline('text-classification', model='distilbert-base-uncased-finetuned-sst-2-english')

def recognize_intent(text):
    """
    Recognize the intent of the input text.
    """
    intent_result = intent_recognition(text)
    return intent_result[0]

def extract_entities(text):
    """
    Extract entities from the input text using spaCy.
    """
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def maintain_context(conversation_history):
    """
    Maintain and return the context from the conversation history.
    """
    context = " ".join(conversation_history)
    return context

# Sample conversation
conversation_history = [
    "I want to book a flight.",
    "Where would you like to go?",
    "New York.",
    "When do you want to go?",
    "July 10th."
]

# User's current input
user_input = "I want to book a train to india on July 10th at 9.30 pm with my friend kishore"

# Recognize intent
intent = recognize_intent(user_input)
print(f"Intent: {intent['label']} with confidence {intent['score']:.2f}")

# Extract entities
entities = extract_entities(user_input)
print("Entities:")
for entity in entities:
    print(f" - {entity[0]}: {entity[1]}")

# Maintain context
context = maintain_context(conversation_history)
print(f"Context: {context}")
