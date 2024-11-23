function sendMessage() {
    const chatbox = document.getElementById('chatbox');
    const userInput = document.getElementById('userInput').value.trim(); // Trim to avoid blank spaces

    if (userInput !== "") {
        // Create a new user message element with user icon
        const userMessage = document.createElement('div');
        userMessage.classList.add('user-message');
        userMessage.innerHTML = `
             <!-- User Icon -->
            <p>${userInput}</p>
            <img src="author2.jpg" alt="User Logo" class="chat-logo">
            <span class="timestamp">${formatTime(new Date())}</span> <!-- User Timestamp -->
        `;

        // Append user message to the chatbox
        chatbox.appendChild(userMessage);

        // Scroll chatbox to the bottom
        chatbox.scrollTop = chatbox.scrollHeight;

        // Clear input field after sending message
        document.getElementById('userInput').value = "";

        // Simulate bot response after a delay
        setTimeout(() => {
            const botMessage = document.createElement('div');
            botMessage.classList.add('bot-message');
            botMessage.innerHTML = `
                <img src="logo.png" alt="Bot Logo" class="chat-logo"> <!-- Bot Icon -->
                <p>Thanks for your input! Here’s how I can assist: ${generateBotResponse(userInput)}</p>
                
                <span class="timestamp">${formatTime(new Date())}</span> <!-- Bot Timestamp -->
            `;

            // Append bot message to the chatbox
            chatbox.appendChild(botMessage);

            // Scroll chatbox to the bottom after bot response
            chatbox.scrollTop = chatbox.scrollHeight;
        }, 1000);
    }
}

// Function to format time to 12-hour format
function formatTime(date) {
    return date.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: 'numeric',
        hour12: true
    });
}

// Function to generate a bot response based on user input
function generateBotResponse(userInput) {
    // Add logic for different responses (you can expand this logic)
    switch (userInput.toLowerCase()) {
        case "how are you?":
            return "I'm just a bot, but I'm doing great! How can I help you?";
        case "help":
            return "Sure! Please tell me how I can assist you today.";
        default:
            return "I’m not sure about that. Could you provide more details?";
    }
}

function handleOption(optionText) {
    const chatbox = document.getElementById('chatbox');

    // Create a new user message element with user icon for the option
    const userMessage = document.createElement('div');
    userMessage.classList.add('user-message');
    userMessage.innerHTML = `
        
        <p>${optionText}</p>
        <img src="author2.jpg" alt="User Logo" class="chat-logo"> <!-- User Icon -->
        <span class="timestamp">${formatTime(new Date())}</span> <!-- User Timestamp -->
    `;

    // Append the user's choice to the chatbox
    chatbox.appendChild(userMessage);

    // Scroll chatbox to the bottom
    chatbox.scrollTop = chatbox.scrollHeight;

    // Simulate bot response after a delay
    setTimeout(() => {
        const botMessage = document.createElement('div');
        botMessage.classList.add('bot-message');
        botMessage.innerHTML = `
            <img src="logo.png" alt="Bot Logo" class="chat-logo"> <!-- Bot Icon -->
            <p>Great choice! Let me help you with: ${optionText}</p>
            
            <span class="timestamp">${formatTime(new Date())}</span> <!-- Bot Timestamp -->
        `;

        // Append bot message to the chatbox
        chatbox.appendChild(botMessage);

        // Scroll chatbox to the bottom after bot response
        chatbox.scrollTop = chatbox.scrollHeight;
    }, 1000);
}

