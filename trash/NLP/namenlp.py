import spacy

# Load a larger spaCy model that includes more entities
nlp = spacy.load("en_core_web_lg")

def extract_human_names(text):
    doc = nlp(text)
    human_names = []
    
    # Iterate through named entities
    for ent in doc.ents:
        if ent.label_ == 'PERSON' and ' ' in ent.text:  # Ensure the entity has more than one word
            human_names.append(ent.text)
    
    # Custom rule to identify human names with possessive form 's
    for token in doc:
        if token.dep_ == 'poss' and token.head.pos_ == 'NOUN' and token.head.head.pos_ == 'VERB':
            human_names.append(f"{token.text} {token.head.text}'s")
    
    return human_names

# Example usage
user_input = "hey iam sanjay kalaiyarasan's friend"
names = extract_human_names(user_input)
print("Human Names:", names)
