import React, { useState, useEffect } from "react";
import io from 'socket.io-client';
import './App.css';

const socket = io('http://localhost:8000');

function App() {
  const [pictureStatus, setPictureStatus] = useState("");
  const [text, setText] = useState(null);
  const [response, setResponse] = useState(null);


  useEffect(() => {
    socket.on('connect', () => console.log('Connected:', socket.id));
    socket.on('picture_taken', data => {
      setPictureStatus(data.message);
      setTimeout(() => setPictureStatus(""), 3000); // Clear status after 3 seconds
    });
    return () => {
      socket.off('picture_taken');
    };
  }, []);

  useEffect(() => {
    socket.on('response', msg => setResponse(msg));
    return () => {
      socket.off('response');    
    };
  }, [])

  const handleChange = e => setText(e.target.value);

  const handleSubmit = e => {
    console.log("Frontend sending message: " + text);
    e.preventDefault(); // prevent page from refreshing
    //React -> Node
    socket.emit('text', text);
    setText("");
  };

  return (
    <div className="App">
      <form className="message-form" onSubmit={handleSubmit}>
          <h1>Send a message</h1>
          <div className="input-group">
            <input
              type="text"
              placeholder="Enter message"
              value={text}
              onChange={handleChange}
              required
            />
          </div>
          <button type="submit" className="message-button">
            Send
          </button>
        </form>
      <h2>Response: {response} </h2>
    </div>
  );
}

export default App;
