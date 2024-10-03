from flask import Flask, request, jsonify, render_template
import ollama

app = Flask(__name__)

# In-memory conversation storage
conversation_memory = {}

# Function to update the conversation memory with user and AI responses
def update_memory(user_id, role, content):
    if user_id not in conversation_memory:
        conversation_memory[user_id] = []
    conversation_memory[user_id].append(f"{role}: {content}")

# Function to generate a response using Ollama
def handle_query(user_id, user_input):
    past_interactions = "\n".join(conversation_memory.get(user_id, [])[-5:])
    prompt = f"""
You are an expert travel assistant. Below is a conversation with a user. Please respond warmly if they greet you (e.g., "hi", "hello", "hey"). After greeting, help them with their travel plans if relevant.
If the query is not related to travel, politely remind the user to stay on the topic of travel.

Past Conversation:
{past_interactions}

User Query: "{user_input}"
    """
    response = ollama.chat(model='llama3.1', messages=[{'role': 'user', 'content': prompt}])
    ai_response = response['message']['content']

    # Update memory
    update_memory(user_id, 'User', user_input)
    update_memory(user_id, 'AI', ai_response)

    return ai_response

# Route to serve the index page
@app.route('/')
def index():
    return render_template('index.html')  # Ensure the index.html file is placed in a 'templates' folder

# Route to handle the AI query
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_id = 1  # Use session ID or user ID in a real app
    user_input = data.get('question')

    ai_response = handle_query(user_id, user_input)
    return jsonify({'answer': ai_response})

if __name__ == "__main__":
    app.run(debug=True)
