import React, { useState, useEffect } from "react";
import io from 'socket.io-client';
import reactImg from "./downloaded_image.jpg"
import sound from "./audio_discription.mp3"
import './App.css';
import useSound from 'use-sound'


const socket = io('http://localhost:8000');

function App() {
  const [pictureStatus, setPictureStatus] = useState();
  const [text, setText] = useState(null);
  const [response, setResponse] = useState(null);
  const [temp, setTempr] = useState(null);
  const [humidity, setHumidity] = useState(null);
  const [lumen, setLumitity] = useState(null);
  const [distance, setDistance] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [playSound] = useSound(sound);


  useEffect(() => {
    socket.on('connect', () => console.log('Connected:', socket.id));
    socket.on('picture_taken', data => {
      //setPictureStatus(data.message);
      //setTimeout(() => setPictureStatus("http://localhost:8000/images/downloaded_image.jpg"), 3000); // Clear status after 3 seconds
      let discriptionAudio = new Audio('audio_discription.mp3');
      setAudioUrl('audio_discription.mp3');
      discriptionAudio.play();
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

  useEffect(() => {
    socket.on('temp', msg => setTempr(msg))
    socket.on('light', msg => setLumitity(msg))
    socket.on('humidity', msg => setHumidity(msg))
    socket.on('ultrasonic', msg => setDistance(msg))
  })

  const handleChange = e => setText(e.target.value);

  const handleSubmit = e => {
    console.log("Frontend sending message: " + text);
    e.preventDefault(); // prevent page from refreshing
    //React -> Node
    socket.emit('text', text);
    setText("");
  };

  const takePic = () => {
    console.log("taking a picture");
    socket.emit('take_picture');
  }

  return (
    <div className="Control Center">
      <h1>Unit 404</h1>
      <div className="temp">
        <h2>Temprature: {temp}</h2>
        <button type="button" onClick={() => socket.emit('tempRequest', temp + " Degrees")}>Send Temprature</button>
      </div>
      <div className="humidity">
        <h2>Humidity: {humidity}</h2>
          <button type="button" onClick={() => socket.emit('humidityRequest', humidity + " % Humid")}>Send humidity</button>
      </div>
      <div className="lumens">
        <h2>Lumens: {lumen}</h2>
        <button type="button" onClick={() => socket.emit('lumenRequest', lumen + " lumens")}>Send lumens</button>
      </div>
      <div className="distances">
        <h2>Distance from target: {distance}</h2>
        <button type="button" onClick={() => socket.emit('distanceRequest', distance + " cm")}>Send distance</button>
      </div>
      <div>
        <form className="message-fo" onSubmit={handleSubmit}>
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
      </div>
      <button type="button" onClick={takePic}>
        Take a picture
      </button>
      <button type = "button" onClick = {() => playSound()}>
        Play audio discription
      </button>
      <img src={reactImg}/>
    </div>
  );
}

export default App;
