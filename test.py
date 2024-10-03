import ollama

# Dictionary to store conversation context for each user (using a session ID or user ID)
conversation_memory = {}

# Function to update the conversation memory with user and AI responses
def update_memory(user_id, role, content):
    if user_id not in conversation_memory:
        conversation_memory[user_id] = []
    conversation_memory[user_id].append(f"{role}: {content}")

# Function to generate a response using Ollama, with memory included in the prompt
def handle_query(user_id, user_input):
    # Fetch past interactions (last 5 exchanges to keep prompt size manageable)
    past_interactions = "\n".join(conversation_memory.get(user_id, [])[-5:])

    # Build the prompt including memory and the new user input
    prompt = f"""
You are an expert travel assistant. Below is a conversation with a user. Please respond warmly if they greet you (e.g., "hi", "hello", "hey"). After greeting, help them with their travel plans if relevant. 
If the query is not related to travel, politely remind the user to stay on the topic of travel.

Past Conversation:
{past_interactions}

User Query: "{user_input}"
    """
    
    # Send the prompt to the model
    response = ollama.chat(model='llama3.1', messages=[{'role': 'user', 'content': prompt}])
    
    # Get the AI's response
    ai_response = response['message']['content']
    
    # Update the memory with the new input and response
    update_memory(user_id, 'User', user_input)
    update_memory(user_id, 'AI', ai_response)

    return ai_response

if __name__ == "__main__":
    # Assign a unique user ID (for simplicity, we use 1 here; in real-world apps, use session ID or user account)
    user_id = 1
    
    print("AI: Welcome to the AI travel assistant. Ask me a question about your travel plans!")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("AI: Goodbye! Safe travels!")
            break

        # Send the user's query to Ollama and pass the user ID for memory
        response = handle_query(user_id, user_input)
        print(f"AI: {response}")
