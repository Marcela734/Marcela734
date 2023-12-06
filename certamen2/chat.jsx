import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const ChatComponent = () => {
  const [userQuestion, setUserQuestion] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatContainerRef = useRef(null);

  const sendMessage = async () => {
    if (!userQuestion.trim()) {
      // Evitar enviar mensajes vacíos
      return;
    }
  
    try {
      setUserQuestion(''); // Limpiar el campo de texto antes de enviar el mensaje
      setLoading(true); // Activar la animación de carga
  
      const apiUrl = 'http://api.localhost/chat';
      const newChatHistory = [...chatHistory, { user: userQuestion }];
      setChatHistory(newChatHistory);
  
      // Enviar el mensaje al backend
      const res = await axios.post(apiUrl, { query: userQuestion });
      console.log('Respuesta del servidor:', res.data);
  
      const botResponse = (res.data && res.data.text) ? res.data.text : 'Respuesta no reconocida';
      const updatedChatHistory = [...newChatHistory, { bot: botResponse }];
      setChatHistory(updatedChatHistory);
    } catch (error) {
      console.error('Error al enviar mensaje:', error);
    } finally {
      setLoading(false); // Desactivar la animación de carga
    }
  };
  

  const handleSendMessage = async (e) => {
    e.preventDefault();
    await sendMessage();
  };

  const handleInputKeyDown = (e) => {
    // Si se presiona Enter y no hay un salto de línea, enviar el mensaje
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault(); // Evitar el salto de línea en el input
      sendMessage();
    }
  };

  useEffect(() => {
    chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
  }, [chatHistory]);

  return (
    <div className="chat-app">
      <div className="chat-header">
        <img src="/logo3.png" alt="Logo" className="logo-image" />
        <h2 className="chat-title">Chatbot Facing UV</h2>
      </div>
      <div className="chat-history-container" ref={chatContainerRef}>
        <ul className="chat-history">
          {chatHistory.map((message, index) => (
            <li key={index} className={message.user ? 'message user-message' : 'message bot-message'}>
              <div className="message-content">{message.user ? message.user : message.bot}</div>
            </li>
          ))}
          {loading && (
            <li className="message bot-message loading-message">
              <div className="message-content">Cargando...</div>
            </li>
          )}
        </ul>
      </div>
      <div className="chat-input-container">
        <form className="chat-input-form" onSubmit={handleSendMessage}>
          <input
            type="text"
            placeholder="Escribe un mensaje..."
            value={userQuestion}
            onChange={(e) => setUserQuestion(e.target.value)}
            onKeyDown={handleInputKeyDown}
            className="chat-input" // Agrega la clase "chat-input"
          />

          <button type="submit" className="send-button">Enviar</button>

        </form>
      </div>
    </div>
  );
};

export default ChatComponent;
