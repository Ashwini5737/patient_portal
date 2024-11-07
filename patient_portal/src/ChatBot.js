import React, { useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom'; // Import useParams
import './ChatBot.css';
function ChatBot() {
    const { id: patientId } = useParams(); // Use useParams to get patientId from URL
    const [userMessage, setUserMessage] = useState('');
    const [chatResponses, setChatResponses] = useState([]);
    const [errorMessage, setErrorMessage] = useState(''); // State for error messages

    const handleSendMessage = async () => {
        if (!userMessage.trim()) return; // Prevent sending empty messages
        try {
            const response = await axios.post(`http://127.0.0.1:5001/chat/${patientId}`, { message: userMessage });
            setChatResponses([...chatResponses, { user: userMessage, bot: response.data.response }]);
            setUserMessage(''); // Reset input field after sending
            setErrorMessage(''); // Clear any previous error messages
        } catch (error) {
            console.error('Error sending message:', error);
            setErrorMessage('Failed to send message. Please try again.'); // Set error message
        }
    };

    return (
        <div className="chatbot">
            <div className="chat-window">
                {chatResponses.map((chat, index) => (
                    <div key={index}>
                        <p><strong>User:</strong> {chat.user}</p>
                        <p><strong>Bot:</strong> {chat.bot}</p>
                    </div>
                ))}
                {errorMessage && <p className="error-message">{errorMessage}</p>} {/* Display error message */}
            </div>
            <input
                type="text"
                value={userMessage}
                onChange={(e) => setUserMessage(e.target.value)}
                placeholder="Type your message..."
            />
            <button onClick={handleSendMessage}>Send</button>
        </div>
    );
}

export default ChatBot;
