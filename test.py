from transformers import BertTokenizer, BertForSequenceClassification
import torch
import ollama

# Load BERT tokenizer and model for intent classification
bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)  # Assume 2 labels: travel-related, not travel-related

# Function to generate a response using the LLaMA model via ollama
def ask_question(user_input):
    response = ollama.chat(model='llama3.1', messages=[{'role': 'user', 'content': user_input}])
    return response['message']['content']

if __name__ == "__main__":
    print("Welcome to the AI travel assistant. Ask me a question about your travel plans!")
    
    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye! Safe travels!")
            break
        

        response = ask_question(user_input)
        print(f"AI: {response}")
