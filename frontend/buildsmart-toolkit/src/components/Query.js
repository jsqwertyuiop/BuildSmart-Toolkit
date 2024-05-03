import axios from 'axios';
import {React, useState} from 'react';
import { Link, useNavigate } from 'react-router-dom';

export function Query(props) {
    const [energyCSV, setEnergyCSV] = useState(null);
    const [city, setCity] = useState(null);
    const [state, setState] = useState(null);
    const [timeOfPredict, setTimeOfPredict] = useState(null);
    const [chatgptResponse, setChatgptResponse] = useState(null);
    const [csvData, setCSVData] = useState(null)
    let navigate = useNavigate();

    const handleEnergyCSV = (e) => {
        setEnergyCSV(e.target.files[0]);
        console.log("I am here")
        const formData = new FormData();
        formData.append("file", e.target.files[0]);
        const response = axios.post('http://127.0.0.1:5000/uploadFile', formData, {withCredentials: true}).then(response => {
            setCSVData(response.data.fileContent)
            console.log(`File uploaded successfully: ${response.data.message}`);
        }).catch(error => {
            alert(`File upload failed: ${error.message}`);
        });
    }

    const handleCity = (e) => {
      setCity(e.target.value);
    }

    const handleState = (e) => {
      setState(e.target.value);
    }

    const sendLocationDay = async (e) => {
      
      // e.preventDefault();
      setTimeOfPredict("Day")
      if (city != null && state != null) {
        //  const response = await axios.post('http://127.0.0.1:5000/location', , {withCredentials: true}).then(response => {
        //      console.log(`Location Successfully Sent`);
        //      console.log("Logging in the then:" + response)
        //      return response
        //  }).catch(error => {
        //      alert(`Failed to send location: ${error.message}`);
        //  });

         const chatResponse = await axios.post('http://127.0.0.1:5000/chatbot', {"time": "Day", "location": city + " " + state, 'csv': csvData}, {withCredentials: true}).then(chatResponse => {
             console.log(`ChatBot Prompt Successfully Sent`);
             console.log("Logging in the then:" + chatResponse)
             return chatResponse
         }).catch(error => {
             alert(`Failed to send message: ${error.message}`);
         });
         const weatherResponse = await axios.post('http://127.0.0.1:5000/forecasts', {"location": city + " " + state}, {withCredentials: true}).then(response => {
              console.log(`Weather uploaded successfully: ${response}`);
              return response
          }).catch(error => {
              alert(`File upload failed: ${error.message}`);
          });
        //  console.log(response)
         console.log("received: " + chatResponse.data.response);
         setChatgptResponse(chatResponse.data.response);
         console.log("set the state: " + chatgptResponse);
         const Response = chatResponse.data.response
         const location = city + " " + state
         console.log(Response)
         const weather = weatherResponse.data.forecasts
         console.log(weatherResponse)
         console.log(weather)
         navigate('/predict-day', { state: { city, state, Response, weather} });
       }
    }

    const sendLocationWeek = (e) => {
      setTimeOfPredict("Week")
      // e.preventDefault();
      if (city != null && state != null) {
         const response = axios.post('http://127.0.0.1:5000/location', {"location": city + " " + state}, {withCredentials: true}).then(response => {
             console.log(`Location Successfully Sent`);
         }).catch(error => {
             alert(`Failed to send location: ${error.message}`);
         });

         const chatResponse = axios.post('http://127.0.0.1:5000/chatbot', {"time": "Week", "location": city + " " + state, 'csv': csvData}, {withCredentials: true}).then(chatResponse => {
             console.log(`ChatBot Prompt Successfully Sent`);
         }).catch(error => {
             alert(`Failed to send message: ${error.message}`);
         });
         console.log(chatResponse.response);
         setChatgptResponse(chatResponse);
       }
    }

    return (
      <div>
        <div className="query">
          <h1>Welcome to BuildSmart Toolkit!</h1>
          <p>By providing us with your energy usage and location, 
            we can help you predict your future energy usage and provide strategies to help you save money
            while helping the environment.</p>
          <div className="all-queries">
            <div className="upload-vertical">
              <span class="material-symbols-outlined" style={{fontSize: "50px",}}>bolt</span>
              <h2>Energy Usage</h2>
              <p>Please upload a CSV with your hourly energy usage.</p>
              <div className="upload-energy-CSV">
                <label for="energyCSV" className="upload-file" >Upload CSV</label>
                <input id="energyCSV" className="input-upload" type="file" onChange={handleEnergyCSV}/>
                <br />
              </div>
            </div>
            <div className="upload-vertical">
              <span class="material-symbols-outlined" style={{fontSize: "50px",}}>location_on</span>
              <h2>Location</h2>
              <p>We need your location to access weather forecasts, which may affect future energy usage.</p>
              <div className="buttons">
                <input type="text" name="City" placeholder="City" onChange={handleCity}/><br />
                <input type="text" name="State" placeholder="State" onChange={handleState}/><br />
              </div>
            </div>
          </div>        
        </div>

        <div className="footer">
          <h2>How far do you want to predict?</h2>
          <div className="buttons">
            <button className="predict-button" onClick={sendLocationDay}>1 Day</button>
            <button className="predict-button" onClick={sendLocationWeek}>1 Week</button>
          </div>
        </div>
      </div>
    );
}