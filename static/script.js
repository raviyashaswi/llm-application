const chatLog = document.getElementById('chat-log');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const fileElement = document.getElementById('file');

async function sendMessage() {
    const message = userInput.value.trim();
    const file = fileElement.files[0];
    if (!message && !file) {
        console.warn("No message or file to send.");
        return;
    }
    if (message) {
        displayMessage('user', message);
    }
    if (file) {
        displayMessage('user', `📜 ${file.name}`); 
    }
    const formData = new FormData();
    formData.append('tag', message);
    if (file) {
        formData.append('file', file);
    }
    userInput.value = '';
    fileElement.value = '';
    try {
        const response = await fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            body: formData,
        });

        console.log("Frontend: FormData sent!"); 
        console.log("Frontend: Response object:", response);

        if (response.ok) {
            const rawResponse = await response.text(); 
            console.log("Raw server response:", rawResponse);

            let data;
            try {
                data = JSON.parse(rawResponse);
                displayMessage('bot', data.r);
            } catch (e) {
                console.error("Failed to parse JSON:", e);
                displayMessage('bot', `Server returned unexpected data: ${rawResponse}`);
            }

        } else {
            const errorText = await response.text();
            console.error('Frontend: API request failed:', response.status, response.statusText, errorText);
            displayMessage('bot', `Error from server: ${response.status} ${response.statusText}. Details: ${errorText.substring(0, 100)}...`);
        }
    } catch (error) {
        console.error('Frontend: Error during fetch:', error);
        displayMessage('bot', `Oops! Network or processing error: ${error.message}`);
    }
}

function displayMessage(sender, text) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add(`${sender}-message`);
    const sanitizedText = document.createTextNode(text);
    messageDiv.appendChild(sanitizedText);
    chatLog.appendChild(messageDiv);
    chatLog.scrollTop = chatLog.scrollHeight;
}
// function noAR(event){
//    event.preventDefault();
// }
// Event listeners
sendButton.addEventListener('click', sendMessage,);//noAR);

userInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        sendMessage();
        //noAR();
    }
});
