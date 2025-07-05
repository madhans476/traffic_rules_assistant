const API_BASE_URL = 'http://localhost:8000';

const chatContainer = document.getElementById('chatContainer');
const queryInput = document.getElementById('queryInput');
const askButton = document.getElementById('askButton');
const typingIndicator = document.getElementById('typingIndicator');
const statusIndicator = document.getElementById('statusIndicator');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');

let isFirstMessage = true;

// Auto-resize textarea
queryInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// Check API connection on load
checkApiConnection();

// Event listeners
askButton.addEventListener('click', handleAskQuestion);
queryInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleAskQuestion();
    }
});

async function checkApiConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        if (response.ok) {
            statusText.textContent = 'Online';
            statusDot.style.background = '#4ade80';
        } else {
            throw new Error('API not responding');
        }
    } catch (error) {
        statusText.textContent = 'Offline';
        statusDot.style.background = '#ef4444';
        statusDot.style.animation = 'none';
        console.error('API connection failed:', error);
    }
}

function askSampleQuestion(question) {
    queryInput.value = question;
    handleAskQuestion();
}

async function handleAskQuestion() {
    const query = queryInput.value.trim();

    if (!query) {
        queryInput.focus();
        return;
    }

    // Clear welcome message if this is the first question
    if (isFirstMessage) {
        chatContainer.innerHTML = '';
        isFirstMessage = false;
    }

    // Add user message
    addMessage(query, 'user');
    
    // Clear input and show typing indicator
    queryInput.value = '';
    queryInput.style.height = 'auto';
    setTyping(true);

    try {
        const response = await fetch(`${API_BASE_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                top_k: 10
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        // Simulate some typing time for better UX
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        // Add bot response
        addMessage(data.answer, 'bot');
        
    } catch (error) {
        console.error('Error:', error);
        addMessage('🚨 Sorry, I encountered an error while processing your question. Please make sure the API server is running and try again.', 'bot');
        
        // Update status to offline
        statusText.textContent = 'Offline';
        statusDot.style.background = '#ef4444';
        statusDot.style.animation = 'none';
    } finally {
        setTyping(false);
    }
}

function addMessage(content, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;
    
    messageDiv.appendChild(messageContent);
    chatContainer.appendChild(messageDiv);
    
    // Scroll to bottom smoothly
    chatContainer.scrollTo({
        top: chatContainer.scrollHeight,
        behavior: 'smooth'
    });
}

function setTyping(isTyping) {
    if (isTyping) {
        typingIndicator.style.display = 'block';
        chatContainer.appendChild(typingIndicator);
        askButton.disabled = true;
        askButton.style.opacity = '0.6';
    } else {
        typingIndicator.style.display = 'none';
        askButton.disabled = false;
        askButton.style.opacity = '1';
    }
    
    // Scroll to bottom
    chatContainer.scrollTo({
        top: chatContainer.scrollHeight,
        behavior: 'smooth'
    });
}

// Auto-focus on input when page loads
window.addEventListener('load', () => {
    queryInput.focus();
});

// Keep connection status updated
setInterval(checkApiConnection, 30000); // Check every 30 seconds
