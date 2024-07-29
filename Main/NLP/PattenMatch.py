import re

# Sample sentences
sentences = [
    "Make a call to kishore.",
    "Call kishore immediately.",
    "Please call john at 5 PM.",
    "She said call michael after the meeting."
]

# Regex pattern to find the name after 'call'
pattern = r"\bcall\b\s+(to\s+)?([A-Z][a-z]*)"

# Extract names
for sentence in sentences:
    match = re.search(pattern, sentence, re.IGNORECASE)
    if match:
        name = match.group(2)  # Group 2 contains the name
        print(f"Name extracted: {name}")
    else:
        print("No match found.")
