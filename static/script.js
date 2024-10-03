function sendMessage() {
    const input = document.getElementById('user-input').value.trim();
    const messagesDiv = document.getElementById('messages');

    if (!input) {
        return; // Don't send an empty message
    }

    // Display user message
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user');
    userMessage.innerText = input;
    messagesDiv.appendChild(userMessage);

    // Fetch AI response
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: input })
    })
    .then(response => response.json())
    .then(data => {
        // Display AI message
        const aiMessage = document.createElement('div');
        aiMessage.classList.add('message', 'ai');
        aiMessage.innerText = data.answer;
        messagesDiv.appendChild(aiMessage);

        // Clear input field
        document.getElementById('user-input').value = '';

        // Auto-scroll to the latest message
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    })
    .catch(error => console.error('Error:', error));
}
