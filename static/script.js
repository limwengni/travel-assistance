function sendMessage() {
    const input = document.getElementById('user-input').value;
    const messagesDiv = document.getElementById('messages');

    // Display user message
    messagesDiv.innerHTML += `<div class="message user">${input}</div>`;

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
        const aiMessage = `<div class="message ai">${data.answer}</div>`;
        messagesDiv.innerHTML += aiMessage;
        document.getElementById('user-input').value = '';  // Clear input
    });
}
