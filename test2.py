import spacy
from spacy.matcher import Matcher

# Load spaCy's pre-trained English model
nlp = spacy.load("en_core_web_sm")

# Input text
text = """
1. Shibuya Crossing
One of the world’s busiest pedestrian crossings, it’s an iconic spot known for its chaotic yet organized flow of people. It's a great place to experience Tokyo’s urban energy.
2. Hachiko Statue
A famous meeting point near Shibuya Station, this statue honors Hachiko, the loyal dog who waited for his owner every day even after his death.
3. Shibuya Scramble Square
A skyscraper with observation decks like Shibuya Sky offering panoramic views of the city, especially stunning at night.
4. Shibuya Center-gai
A bustling shopping street filled with trendy fashion stores, cafés, restaurants, and entertainment spots, it's a hub for youth culture and street fashion.
5. Shibuya 109
A trendy shopping mall known for its cutting-edge fashion, especially popular with younger crowds looking for unique and stylish clothing.
"""

# Process the text using spaCy
doc = nlp(text)

# Initialize Matcher
matcher = Matcher(nlp.vocab)

# Define patterns for matching place names
patterns = [
    [{"IS_TITLE": True}, {"IS_TITLE": True}],  # Two consecutive title case words
    [{"IS_TITLE": True}, {"IS_TITLE": True, "OP": "?"}, {"IS_TITLE": True}],  # Three words (with one optional)
]

# Add patterns to matcher
for pattern in patterns:
    matcher.add("PLACE_NAME", [pattern])

# Find matches in the doc
matches = matcher(doc)

# Extract matched place names
matched_place_names = {doc[start:end].text for match_id, start, end in matches}

# Sort and print the extracted place names
print("Extracted Place Names:")
for place in sorted(matched_place_names):
    print(place)
