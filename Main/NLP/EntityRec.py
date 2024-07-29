from transformers import pipeline

# Load the pre-trained NER pipeline
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

# Sample text for entity extraction
text = "Barack Obama was born on August 4, 1961, in Honolulu, Hawaii. He served as the 44th President of the United States."

# Extract entities
entities = ner_pipeline(text)

# Display the extracted entities
for entity in entities:
    print(f"Entity: {entity['word']}, Label: {entity['entity_group']}, Score: {entity['score']:.2f}")
