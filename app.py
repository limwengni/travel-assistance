from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, AutoModelForCausalLM, BertTokenizer, BertModel
import torch

app = Flask(__name__)

# Load BERT tokenizer and model for intent classification or structured processing
bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained('bert-base-uncased')

# Load Mistral 7B tokenizer and model for conversational responses
mistral_tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
mistral_model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1")

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

    # Tokenize and process the input with Mistral 7B
    mistral_inputs = mistral_tokenizer(user_input, return_tensors='pt')

    # Generate a response using Mistral 7B
    with torch.no_grad():
        outputs = mistral_model.generate(**mistral_inputs, max_length=150)

    # Decode the generated response
    answer = mistral_tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return jsonify({'answer': answer})

if __name__ == "__main__":
    app.run(debug=True)
