console.log('Script loaded successfully!');

class Chatbot {
    constructor() {
        this.chatBox = document.getElementById('chat-box');
        this.userInput = document.getElementById('user-input');
        this.selectedSymptoms = new Set();
        this.responses = {
            'Emergency Help': "If this is a medical emergency, please call emergency services immediately (911 or your local emergency number).",
            'Medical History': "To check your medical history, please log in to your account or consult with your healthcare provider.",
            'Book Appointment': "To book an appointment, please select your symptoms first so I can recommend the appropriate specialist."
        };
    }

    // Add message to chat
    addMessage(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        if (sender === 'bot') {
            messageDiv.innerHTML = `
                <span class="bot-icon">⚕️</span>
                <div class="message-content">${message}</div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="message-content">${message}</div>
                <i class="fas fa-user user-icon"></i>
            `;
        }
        
        this.chatBox.appendChild(messageDiv);
        this.scrollToBottom();
    }

    // Scroll chat to bottom
    scrollToBottom() {
        this.chatBox.scrollTop = this.chatBox.scrollHeight;
    }

    // Toggle symptom selection
    toggleSymptom(symptom) {
        if (this.selectedSymptoms.has(symptom)) {
            this.selectedSymptoms.delete(symptom);
        } else {
            this.selectedSymptoms.add(symptom);
        }
    }

    // Check symptoms and get prediction
    async checkSymptoms() {
        if (this.selectedSymptoms.size === 0) {
            this.addMessage("Please select at least one symptom.", "bot");
            return;
        }

        this.addMessage("Analyzing your symptoms...", "bot");

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    symptoms: Array.from(this.selectedSymptoms)
                })
            });

            const result = await response.json();
            
            if (result.error) {
                this.addMessage(`Error: ${result.error}`, "bot");
                return;
            }

            // Format the prediction message
            let predictionMessage = `
                <strong>Possible Condition:</strong> ${result.disease}<br>
                <strong>Confidence Level:</strong> ${result.confidence}%<br>
                <strong>Recommended Doctor:</strong> ${result.doctor_name}<br>
                <strong>Doctor's Profile:</strong> <a href="${result.doctor_link}" target="_blank">View Profile</a><br><br>
                <strong>Symptoms You Reported:</strong><br>
                ${result.symptoms_present.join(', ')}<br><br>
                <strong>Common Symptoms for this Condition:</strong><br>
                ${result.symptoms_given.join(', ')}
            `;

            this.addMessage(predictionMessage, "bot");
        } catch (error) {
            console.error('Error:', error);
            this.addMessage("Sorry, there was an error processing your symptoms. Please try again.", "bot");
        }
    }

    // Handle quick action button clicks
    handleQuickAction(action) {
        this.addMessage(action, 'user');
        const response = this.responses[action];
        if (response) {
            this.addMessage(response, 'bot');
        }
    }
}

// Initialize chatbot
const chatbot = new Chatbot();

// Load symptoms when page loads
window.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/get_symptoms');
        const data = await response.json();
        const symptomsList = document.getElementById('symptoms-list');
        
        data.symptoms.forEach(symptom => {
            const div = document.createElement('div');
            div.className = 'symptom-item';
            div.innerHTML = `
                <input type="checkbox" id="${symptom}" value="${symptom}">
                <label for="${symptom}">${symptom.replace(/_/g, ' ')}</label>
            `;
            
            const checkbox = div.querySelector('input');
            checkbox.addEventListener('change', () => chatbot.toggleSymptom(symptom));
            
            symptomsList.appendChild(div);
        });
    } catch (error) {
        console.error('Error loading symptoms:', error);
    }
});

// Handle quick action buttons
document.querySelectorAll('.quick-btn').forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        chatbot.handleQuickAction(this.textContent);
    });
});

// Function to check symptoms (called from HTML)
function checkSymptoms() {
    chatbot.checkSymptoms();
}

// Function to send message (called from HTML)
function sendMessage() {
    const message = chatbot.userInput.value.trim();
    if (message) {
        chatbot.addMessage(message, 'user');
        chatbot.userInput.value = '';
        // Add bot response based on message
        setTimeout(() => {
            chatbot.addMessage("I recommend using the symptom checker above to help diagnose your condition.", 'bot');
        }, 500);
    }
}