import './App.css';
import { HeaderSection } from "./components/Header.js";
import Helmet from "react-helmet";
import { useLocation } from "react-router-dom";
import { useState, useEffect } from 'react';
import axios from 'axios';

export function ResultDay() {

  const location = useLocation();
  const [updatedGPTResponse, setUpdatedGPTResponse] = useState(null)

  useEffect(() => {
    
    setUpdatedGPTResponse(location.state.Response)
    console.log("response received")
    console.log("from the result page: " + location.state.Response)

  }, [location.state]);

  // const weatherResponse = axios.post('http://127.0.0.1:5000/forecasts', {location: location.state.location}, {withCredentials: true}).then(response => {
  //     console.log(`Weather uploaded successfully: ${weatherResponse}`);
  // }).catch(error => {
  //     alert(`File upload failed: ${error.message}`);
  // });

  return (
    <div>
      <Helmet>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet" />
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
      </Helmet>
      <HeaderSection />
      <div>
        <div className="query">
          <h1>Your 1 Day Result</h1>
          <div className="all-stats">
            <div className="stats" id="location-stat">
              <h3>Location</h3>
              <p><b>CITY: </b>{location.state.city}</p>
              <p><b>STATE: </b>{location.state.state}</p>
            </div>
            <div className="stats" id="weather-stat">
              <h3>Weather Tomorrow</h3>
              <p>{location.state.weather[0]}</p>
            </div>
          </div>
          <div className="chatgpt-answer">
              {
                updatedGPTResponse && updatedGPTResponse.split('\n').map((line, index) => (
                  <p>
                    {line}
                  </p>
                ))
              }
            {/* <p>{updatedGPTResponse}</p> */}
          </div>
        </div>
      </div>
    </div>
  );
}

export function ResultWeek() {

    const location = useLocation();
    const [updatedGPTResponse, setUpdatedGPTResponse] = useState(null)

    useEffect(() => {
      
      setUpdatedGPTResponse(location.state.Response)
      console.log("response received")
      console.log("from the result page: " + location.state.Response)

    }, [location.state]);

    return (
      <div>
        <Helmet>
          <link rel="preconnect" href="https://fonts.googleapis.com" />
          <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
          <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet" />
          <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
        </Helmet>
        <HeaderSection />
        <div className="query">
          <h1>Your 1 Week Result</h1>
          <div className="all-stats">
            <div className="stats" id="location-stat">
                <h3>Location</h3>
                <p><b>CITY: </b>{location.state.city}</p>
                <p><b>STATE: </b>{location.state.state}</p>
                </div>
                <div className="stats" id="weather-stat">
                <h3>Weather Tomorrow</h3>
                <p>{location.state.weather[0]}</p>
            </div>
          </div>
          <div className="chatgpt-answer">
            <p>{location.state.chatgptResponse}</p>
          </div>
        </div>
      </div>
    );
  }
