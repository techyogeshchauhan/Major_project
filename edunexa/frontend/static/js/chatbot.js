document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('chat-form');
    const input = document.getElementById('user-message');
    const chatBox = document.getElementById('chat-box');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = input.value.trim();
        if (!message) return;

        appendMessage('You', message);
        input.value = '';

        try {
            const res = await fetch('/api/chatbot/message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            const data = await res.json();
            appendMessage('Bot', data.response);
        } catch (err) {
            appendMessage('Bot', 'Error: Could not reach server.');
        }
    });

    function appendMessage(sender, message) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('mb-2');
        msgDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
