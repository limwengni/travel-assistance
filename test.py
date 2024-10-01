from transformers import AutoTokenizer, BertTokenizer, BertModel, pipeline

# Load BERT tokenizer and model for intent classification or structured processing
bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained('bert-base-uncased')

# Create a pipeline for conversational responses using Mistral 7B
mistral_pipeline = pipeline("text-generation", model="alexsherstinsky/Mistral-7B-v0.1-sharded")

def ask_question(user_input):
    # Generate a response using the Mistral pipeline
    mistral_response = mistral_pipeline(user_input, max_length=150, num_return_sequences=1)

    # Extract the generated text
    answer = mistral_response[0]['generated_text']
    return answer

if __name__ == "__main__":
    print("Welcome to the AI travel assistant. Ask me a question about your travel plans!")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye! Safe travels!")
            break
        
        # Get the AI-generated response
        response = ask_question(user_input)
        
        # Display the response
        print(f"AI: {response}")
