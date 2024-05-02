import './App.css';
import { HeaderSection } from "./components/Header.js";
import Helmet from "react-helmet";
import { useLocation } from "react-router-dom";

export function ResultDay() {

  const location = useLocation();

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
              <h1>74°F</h1>
            </div>
          </div>
          <div className="chatgpt-answer">
            <p>Hi there! this is chatgpt and i dont know the answer</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export function ResultWeek() {

    const location = useLocation();

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
                <h1>74°F</h1>
            </div>
          </div>
          <div className="chatgpt-answer">
            <p>By providing us with your energy usage and location, 
                we can help you predict your future energy usage and provide strategies to help you save money
                while helping the environment.</p>
          </div>
        </div>
      </div>
    );
  }
