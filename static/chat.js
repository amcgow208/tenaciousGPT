document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.getElementById('send-button');
    const messageInputField = document.getElementById('message-input');
    const chatHistory = document.getElementById('chat-history');
    const chatSessions = document.querySelectorAll('.chat-session');

    // Event listeners for send button and enter keypress
    sendButton.addEventListener('click', sendMessage);
    messageInputField.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Event listeners for chat sessions
    chatSessions.forEach(session => {
        session.addEventListener('click', function() {
            const sessionId = this.dataset.sessionId; // Use dataset to access data attributes
            loadChatSession(sessionId);
        });
    });

    function sendMessage() {
        const message = messageInputField.value.trim();
        if (message === '') {
            return; // Ignore empty messages
        }

        appendMessage(message, 'message user');
        messageInputField.value = ''; // Clear input field
        sendButton.disabled = true;

        fetch('/process_message', {
            method: 'POST',
            body: JSON.stringify({ message: message }),
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            appendMessage(data.answer, 'message assistant');
        })
        .catch(error => console.error('Error:', error))
        .finally(() => {
            sendButton.disabled = false;
            chatHistory.scrollTop = chatHistory.scrollHeight;
        });
    }

    function appendMessage(text, className) {
        const messageDiv = document.createElement('div');
        messageDiv.textContent = text;
        messageDiv.className = className;
        chatHistory.appendChild(messageDiv);
    }

    function loadChatSession(sessionId) {
        fetch(`/get_chat_history/${sessionId}`)
        .then(response => response.json())
        .then(data => {
            chatHistory.innerHTML = ''; // Clear existing chat history
            data.forEach(entry => {
                appendMessage(entry.message, `message ${entry.sender}`);
            });
        })
        .catch(error => console.error('Error loading chat history:', error));
    }
});
