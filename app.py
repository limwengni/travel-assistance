from flask import Flask, request, jsonify, render_template
from transformers import BertTokenizer, BertModel

# Initialize Flask app
app = Flask(__name__)

# Load BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

@app.route('/')
def home():
    return render_template('index.html')  # Serve your front-end HTML

# API endpoint to process user queries
@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json['question']
    # Tokenization and model inference
    inputs = tokenizer(user_input, return_tensors='pt')
    outputs = model(**inputs)
    # Extract embeddings or perform additional processing here
    return jsonify({'answer': 'Your processed response here'})

if __name__ == "__main__":
    app.run(debug=True)
