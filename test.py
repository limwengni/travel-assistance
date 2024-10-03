import random
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import ollama

# BERT tokenizer and model for intent classification
bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)  # 2 labels: travel-related, not travel-related

# Function to classify user input (travel-related or not)
def classify_intent(user_input):
    inputs = bert_tokenizer(user_input, return_tensors="pt", truncation=True, padding=True)
    outputs = bert_model(**inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    predicted_label = torch.argmax(probabilities).item()
    return predicted_label  # 0 for travel-related, 1 for not travel-related

# Function to generate a response using the LLaMA model via Ollama
def ask_question(user_input):
    response = ollama.chat(model='llama3.1', messages=[{'role': 'user', 'content': user_input}])
    return response['message']['content']

# Function to generate an off-topic response via Ollama dynamically
def get_off_topic_response(user_input):
    prompt = "You are a friendly travel assistant. If a user asks something that is not travel-related, kindly remind them to stay on the topic of travel. Be helpful and polite."
    response = ollama.chat(model='llama3.1', messages=[
        {'role': 'system', 'content': prompt},
        {'role': 'user', 'content': user_input}
    ])
    return response['message']['content']

if __name__ == "__main__":
    print("Welcome to the AI travel assistant. Ask me a question about your travel plans!")
    
    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye! Safe travels!")
            break

        # Classify whether the input is travel-related or not
        intent_label = classify_intent(user_input)

        if intent_label == 0:  # Travel-related
            response = ask_question(user_input)
            print(f"AI: {response}")
        else:  # Not travel-related
            # Generate dynamic off-topic response from Ollama
            off_topic_response = get_off_topic_response(user_input)
            print(f"AI: {off_topic_response}")
