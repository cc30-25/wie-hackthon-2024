// Month and day names
const months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];

// Generate the calendar
const calendarContainer = document.getElementById('calendar-container');
months.forEach((month, monthIndex) => {
    const monthDiv = document.createElement('div');
    monthDiv.className = 'month';
    monthDiv.innerHTML = `<h2>${month}</h2><div class="days"></div>`;
    const daysDiv = monthDiv.querySelector('.days');

    // Get the number of days in the current month
    const daysInMonth = new Date(2024, monthIndex + 1, 0).getDate();

    for (let day = 1; day <= daysInMonth; day++) {
        const dayDiv = document.createElement('div');
        dayDiv.className = 'day';
        dayDiv.dataset.date = `${monthIndex + 1}/${day}`;
        dayDiv.innerText = day;
        daysDiv.appendChild(dayDiv);
    }

    calendarContainer.appendChild(monthDiv);
});

// Chatbot functionality
const openChatbotButton = document.getElementById('openChatbot');
const chatbotModal = document.getElementById('chatbotModal');
const closeChatbot = document.getElementById('closeChatbot');
const chatbox = document.getElementById('chatbox');
const userInput = document.getElementById('userInput');

// Open chatbot modal
openChatbotButton.addEventListener('click', () => {
    chatbotModal.style.display = 'block';
});

// Close chatbot modal
closeChatbot.addEventListener('click', () => {
    chatbotModal.style.display = 'none';
});

// Chatbot interaction
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const input = userInput.value.trim();
        if (input) {
            appendMessage('You', input);
            processChatbotInput(input);
        }
        userInput.value = '';
    }
});

function appendMessage(sender, message) {
    const msgDiv = document.createElement('div');
    msgDiv.textContent = `${sender}: ${message}`;
    chatbox.appendChild(msgDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function processChatbotInput(input) {
    // Parse holiday information
    const match = input.match(/(.+) on (\d+)\/(\d+)/);
    if (match) {
        const holidayName = match[1];
        const month = parseInt(match[2]) - 1;
        const day = parseInt(match[3]);

        // Find and mark the day on the calendar
        const dayDiv = document.querySelector(`.day[data-date="${month + 1}/${day}"]`);
        if (dayDiv) {
            dayDiv.style.backgroundColor = '#FFD700';
            dayDiv.title = holidayName;
            appendMessage('Bot', `Added "${holidayName}" on ${months[month]} ${day}.`);
        } else {
            appendMessage('Bot', "Invalid date. Please try again.");
        }
    } else {
        appendMessage('Bot', "Please use the format 'Holiday Name on MM/DD'.");
    }
}
