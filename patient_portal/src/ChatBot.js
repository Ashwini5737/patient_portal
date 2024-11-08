import React, { useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import './ChatBot.css';

function ChatBot() {
    const { id: patientId } = useParams();
    const [userMessage, setUserMessage] = useState('');
    const [chatResponses, setChatResponses] = useState([]);
    const [errorMessage, setErrorMessage] = useState('');

    const handleSendMessage = async () => {
        if (!userMessage.trim()) return;
        try {
            const response = await axios.post(`http://127.0.0.1:5001/chat/${patientId}`, { message: userMessage });
            // Update chatResponses to include both user and bot messages
            setChatResponses(prevResponses => [
                ...prevResponses, 
                { role: 'user', content: userMessage }, 
                { role: 'bot', content: response.data.response }
            ]);
            setUserMessage('');
        } catch (error) {
            console.error('Error sending message:', error);
            setErrorMessage('Failed to send message. Please try again.');
        }
    };

    return (
        <div className="chat-container">
            <div className="messages-container">
                {chatResponses.map((chat, index) => (
                    <div key={index} className={`message ${chat.role === 'user' ? 'user-message' : 'bot-message'}`}>
                        <p>{chat.content}</p>
                    </div>
                ))}
                {errorMessage && <p className="error-message">{errorMessage}</p>}
            </div>
            <div className="input-container">
                <input
                    type="text"
                    value={userMessage}
                    onChange={(e) => setUserMessage(e.target.value)}
                    placeholder="Type your message..."
                />
                <button onClick={handleSendMessage}>Send</button>
            </div>
        </div>
    );
}

export default ChatBot;