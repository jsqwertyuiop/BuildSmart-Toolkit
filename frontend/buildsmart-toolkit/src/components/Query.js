import axios from 'axios';
import {React, useState} from 'react';

export function Query(props) {
    const [energyCSV, setEnergyCSV] = useState(null);

    const handleEnergyCSV = (e) => {
        setEnergyCSV(e.target.files[0]);
        console.log("I am here")
        const formData = new FormData();
        formData.append("file", e.target.files[0]);
        
        console.log(formData)
        const response = axios.post('http://127.0.0.1:5000/uploadFile', formData).then(response => {
            console.log(`File uploaded successfully: ${response.data.message}`);
        }).catch(error => {
            alert(`File upload failed: ${error.message}`);
        });
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
                <input type="text" name="City" placeholder="City"/><br />
                <input type="text" name="State" placeholder="State"/><br />
              </div>
            </div>
          </div>        
        </div>
      </div>
    );
}