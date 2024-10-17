// src/ChatComponent.js
import React, { useState } from 'react';
import axios from 'axios';
import './ChatComponent.css'; // Importing the CSS file for styling

const ChatComponent = () => {
    const [question, setQuestion] = useState('');
    const [response, setResponse] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const res = await axios.post('http://localhost:5000/chat', { question });
            setResponse(res.data.answer);
        } catch (error) {
            console.error('Error fetching response:', error);
            setResponse('Error fetching response.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="chat-container">
            <h1 className="chat-title">Chatbot</h1>
            <form onSubmit={handleSubmit} className="chat-form">
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Enter your question..."
                    className="chat-input"
                    required
                />
                <button type="submit" className="chat-button" disabled={loading}>
                    {loading ? 'Loading...' : 'Ask'}
                </button>
            </form>
            {response && (
                <div className="chat-response">
                    <h2>Response:</h2>
                    <p>{response}</p>
                </div>
            )}
        </div>
    );
};

export default ChatComponent;
