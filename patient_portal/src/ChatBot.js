import React, { useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import './ChatBot.css';

function ChatBot() {
    const { id: patientId } = useParams();
    const [userMessage, setUserMessage] = useState('');
    const [userFile, setUserFile] = useState(null);
    const [chatResponses, setChatResponses] = useState([]);
    const [errorMessage, setErrorMessage] = useState('');

    const handleSendMessage = async () => {
        if (!userMessage.trim() && !userFile) return;

        const formData = new FormData();
        formData.append('message', userMessage);
        if (userFile) {
            formData.append('file', userFile);
        }

        try {
            const response = await axios.post(`http://127.0.0.1:5001/chat/${patientId}`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setChatResponses(prevResponses => [
                ...prevResponses,
                { role: 'user', content: userMessage },
                { role: 'bot', content: response.data.response }
            ]);
            setUserMessage('');
            setUserFile(null);
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
                <input
                    type="file"
                    onChange={(e) => setUserFile(e.target.files[0])}
                    accept="image/png, image/jpeg"
                />
                <button onClick={handleSendMessage}>Send</button>
            </div>
        </div>
    );
}

export default ChatBot;
