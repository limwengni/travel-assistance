from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama
import random

app = Flask(__name__)

# Enable CORS for the app
CORS(app)

# Dictionary to store conversation context for each user (using a session ID or user ID)
conversation_memory = {}

# Function to update the conversation memory with user and AI responses
def update_memory(user_id, role, content):
    if user_id not in conversation_memory:
        conversation_memory[user_id] = []
    
    # Append the new message
    conversation_memory[user_id].append(f"{role}: {content}")
    
    # Limit to last 10 messages
    if len(conversation_memory[user_id]) > 10:
        conversation_memory[user_id] = conversation_memory[user_id][-10:]

# Function to generate a response using Ollama, with memory included in the prompt
def handle_query(user_id, user_input):
    # Fetch past interactions (last 3 exchanges to keep prompt size manageable)
    past_interactions = "\n".join(conversation_memory.get(user_id, [])[-3:])

    prompt = f"""
    You are an expert travel assistant named Travis. Please respond warmly if they greet you and help them with their travel plans if relevant. If the query is not related to travel, politely remind the user to stay on the topic of travel. 

    Remember, the user is asking about travel topics.

    Past Conversation:
    {past_interactions}

    User Query: "{user_input}"
    """
    
    # Send the prompt to the model
    response = ollama.chat(model='llama3.2:1b', messages=[{'role': 'user', 'content': prompt}]) #llama3.1 llama3.2:1b
    
    # Get the AI's response
    ai_response = response['message']['content']
    
    # Update the memory with the new input and response
    update_memory(user_id, 'User', user_input)
    update_memory(user_id, 'AI', ai_response)

    return ai_response

# Prompts to start conversation with the travel assistant
static_prompts = [
    "What are the must-visit places in Paris?",
    "What’s so special about Tokyo?",
    "How can I plan a 3-day trip to Rome?",
    "Where should I go for a weekend getaway in New York?",
    "What are the top attractions in London?",
    "Can you recommend some activities in Sydney?",
    "What hidden gems are in Bali?",
    "What should I pack for a trip to the Maldives?",
    "How do I navigate public transport in Berlin?",
    "What cultural experiences should I try in Mexico City?",
    "Best beaches to visit in Thailand?",
    "What are the historical sites in Athens?",
    "How to experience the nightlife in Barcelona?",
    "What outdoor activities can I do in Canada?",
    "What are the best local dishes in Italy?",
    "How can I travel on a budget in Europe?",
    "What’s the best way to explore Iceland?",
    "What wildlife experiences can I have in Africa?",
    "What are the top family-friendly destinations?",
    "What are some romantic getaways in Asia?",
    "How to plan a road trip across the USA?",
    "What unique traditions can I experience in India?",
    "What should I know before visiting Egypt?",
    "How can I enjoy a solo trip to New Zealand?",
    "What are the best hiking trails in South America?",
    "What are the must-see art museums in Europe?",
    "How to choose the right travel insurance?",
    "What are the top wine regions to visit?",
    "How can I find local food markets in cities?",
    "What are some tips for traveling with pets?",
    "What are the best ski resorts in North America?",
    "What festivals should I attend in Brazil?",
    "How to find hidden gems in large cities?",
    "What are the best apps for travel planning?",
    "How can I make the most of a layover?",
    "What are the top 10 landmarks in the world?",
    "How to experience authentic local culture while traveling?",
    "What are some eco-friendly travel options?",
    "What are the best travel hacks to save money?",
    "How to deal with language barriers while traveling?",
    "What are the top shopping destinations around the world?",
    "How can I find good deals on flights?",
    "What are some safety tips for traveling abroad?",
    "How to stay connected while traveling internationally?",
    "What are the best travel destinations for food lovers?",
    "How to plan a family vacation on a budget?",
    "What unique experiences can I find in the Arctic?",
    "What are the best places for adventure sports?",
    "How to find local guides for unique experiences?",
    "What should I know about customs and etiquette in different countries?",
    "What are the best resources for solo travelers?",
    "How to create a travel itinerary that works for me?",
    "What are the top travel trends this year?",
    "How to handle travel emergencies and unexpected situations?",
    "What are the best locations for photography enthusiasts?",
    "What are some must-have travel gear for adventurers?",
    "How can I volunteer while traveling?",
]

@app.route('/api/prompts', methods=['GET'])
def generate_prompts():
    # Select 2 static prompts from the list
    selected_static_prompts = random.sample(static_prompts, min(4, len(static_prompts)))

    # Return the static prompts as a JSON response
    return jsonify(selected_static_prompts), 200


@app.route('/api/message', methods=['POST'])
def message():
    user_id = request.json.get('user_id', 1)  # Default to user_id 1 for simplicity
    user_input = request.json.get('message')

    if user_input:
        ai_response = handle_query(user_id, user_input)
        return jsonify({'response': ai_response}), 200
    else:
        return jsonify({'error': 'No message provided'}), 400

if __name__ == "__main__":
    app.run(debug=True)
