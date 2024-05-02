from flask import Flask, request, jsonify
import openai
import os
import requests
import math
import csv
import pandas as pd
from geopy.geocoders import Nominatim
import certifi #for SSL certificate verification for MacOS
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}
CORS(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/uploadFile', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        csv_as_text = ""
        # Temporary untested CSV to Sting code
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                csv_as_text += ','.join(row) + '\n'
        print(csv_as_text)
        return jsonify({'message': f'{filename} uploaded and processed successfully'}), 200
    else:
        return jsonify({'message': 'Invalid file type'}), 400


@app.route('/chatbot', methods=['POST'])
def chatbot_response():
    user_message = request.json.get('message')
    chatgpt_response = chat_with_chatGPT(user_message)
    return jsonify({'response': chatgpt_response})

def chat_with_chatGPT(prompt):
    model = "gpt-3.5-turbo"
    openai.api_key = "sk-proj-zfZq8suoT0gfsWt4LakVT3BlbkFJP6VmY4fLs0p3KeOrKZoD"
    response = openai.chat.completions.create(
        model=model,
        messages=[{'role': 'user', "content": prompt}],
        max_tokens=100
    )
    #retrieves choices list, and gets first choice (as usually only one choice is generated)
    #then we specify the response type, which is text
    output = response.choices[0].message.content
    if (model == "gpt-3.5-turbo"):
        print("Output tokens used: ", math.ceil(len(output)/3.75))
        print("Output cost (cents): ", math.ceil(len(output)/3.75)/1000000 * 150)
    elif (model == "gpt-4-turbo"):
        print("Output tokens used: ", math.ceil(len(output)/3.75))
        print("Output cost (cents): ", math.ceil(len(output)/3.75)/1000000 * 3000)
    return output

def get_coords(location): #returns latitude and longitude of city, state for weather API
    geolocator = Nominatim(user_agent="energy-predictor")
    location = geolocator.geocode(str(location))
    return location.latitude, location.longitude

def get_nws_gridpoints(latitude, longitude): #returns gridpoints for use in weather API
    response = requests.get(f"https://api.weather.gov/points/{latitude},{longitude}")
    data = response.json()
    return data['properties']['gridId'], data['properties']['gridX'], data['properties']['gridY']

def get_weekly_forecast(grid_id, grid_x, grid_y): #returns weekly forecast for location
    response = requests.get(f"https://api.weather.gov/gridpoints/{grid_id}/{grid_x},{grid_y}/forecast")
    data = response.json()
    return data['properties']['periods']

@app.route('/location', method=['POST'])
def location():
    location = request.json.get('location')
    latitude, longitude = get_coords(location)
    print("Latitude: ", latitude, "Longitude: ", longitude)
    grid_id, grid_x, grid_y = get_nws_gridpoints(latitude, longitude)
    print("Grid ID: ", grid_id, "Grid X: ", grid_x, "Grid Y: ", grid_y)
    forecast = get_weekly_forecast(grid_id, grid_x, grid_y)
    for i in range(14): #prints out morning and night forecast for the next 7 days
        print("Date: ", forecast[i]['name'])
        print("Forecast for the day: ", forecast[i]['detailedForecast'])

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': "Welcome to BuildSmart-ToolKit! We are here to help you save energy."}), 200


@app.route('predict', method=['POST'])
def predict():
    return jsonify({'message': 'We are predicting your energy consumption now'})

if __name__ == '__main__':
    app.run(debug=True)
