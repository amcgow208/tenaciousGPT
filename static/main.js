document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.getElementById('send-button');
    const userInputField = document.getElementById('user-input');
    const chatHistory = document.getElementById('chat-history');

    sendButton.addEventListener('click', sendMessage);
    userInputField.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        const userInput = userInputField.value;
        userInputField.value = ''; // Clear input field
        sendButton.disabled = true;

        if (userInput.trim() === '') {
            sendButton.disabled = false;
            return;
        }

        appendMessage(userInput, 'user-message');

        fetch('/process_message', {
            method: 'POST',
            body: JSON.stringify({ message: userInput }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            appendMessage(data.answer, 'bot-response');
        })
        .catch(error => console.error('Error:', error))
        .finally(() => {
            sendButton.disabled = false;
            chatHistory.scrollTop = chatHistory.scrollHeight;
        });
    }

    function appendMessage(message, className) {
        const messageDiv = document.createElement('div');
        messageDiv.textContent = message;
        messageDiv.className = className;
        chatHistory.appendChild(messageDiv);
    }
});
