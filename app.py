from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, BertTokenizer, BertModel, pipeline

app = Flask(__name__)

# Load BERT tokenizer and model for intent classification or structured processing
bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained('bert-base-uncased')

# Create a pipeline for conversational responses using Mistral 7B
mistral_pipeline = pipeline("text-generation", model="alexsherstinsky/Mistral-7B-v0.1-sharded")

@app.route('/')
def home():
    return render_template('index.html')

def is_travel_related(question):
    travel_keywords = [
        'travel', 'trip', 'destination', 'flight', 'hotel',
        'itinerary', 'vacation', 'tour', 'explore', 'adventure',
        'sightseeing', 'traveling', 'journey', 'road trip',
        'experience', 'recommendations', 'places to visit'
    ]
    travel_phrases = [
        "where should I go", "best places", "things to do", 
        "what to see", "plan my trip", "how to travel"
    ]
    
    return any(keyword in question.lower() for keyword in travel_keywords) or \
           any(phrase in question.lower() for phrase in travel_phrases)

def is_greeting(question):
    greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']
    return any(greet in question.lower() for greet in greetings)

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json['question']
    
    # Check if the question is travel-related
    if not is_travel_related(user_input):
        return jsonify({'answer': "I'm not sure about that. But I can definitely help you plan a trip. Where would you like to go?"})

    # Use BERT to process the input if needed (for intent classification or extraction)
    bert_inputs = bert_tokenizer(user_input, return_tensors='pt')
    bert_outputs = bert_model(**bert_inputs)

    # Generate a response using the Mistral pipeline
    mistral_response = mistral_pipeline(user_input, max_length=150, num_return_sequences=1)

    # Extract the generated text
    answer = mistral_response[0]['generated_text']
    
    return jsonify({'answer': answer})

if __name__ == "__main__":
    app.run(debug=True)