from flask import Flask, request, jsonify, session
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
import asyncio
import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}
app.config['SESSION_COOKIE_NAME'] = 'session'
app.config['SESSION_COOKIE_SECURE'] = False  # Use True only if you are using HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
# CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = "cse551_final_project"
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


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
        session['csv_string'] = csv_as_text
        session.modified = True
        print("THIS IS SESSION DATA FOR CSV STRING" + session['csv_string'])
        print(csv_as_text)
        return jsonify({'fileContent' : csv_as_text}), 200
    else:
        return jsonify({'message': 'Invalid file type'}), 400


@app.route('/chatbot', methods=['POST'])
def chatbot_response():
    predict_string = request.json.get('time')
    location = request.json.get('location')
    csv_string = request.json.get('csv')
    x = datetime.datetime.now()
    x = x.strftime("%x")
    if(predict_string == "Week"):
        predict_string = "24 hours of" + x + ", for the next 7 days"
        weather = weather_data(location, 7)
    else:
        predict_string = "24 hours of" + x
        weather = weather_data(location, 1)
    user_message = prompt = f"""You are an energy predictor trying to predict energy usage of a residential building given hourly energy consumption data in kWhs and the location of the building. You will be predicting energy usage for the following day or week. Based on the provided data and the prediction, you will identify potential flaws in the energy usage and provide potential solutions to conserve energy. Then, using the weather data for the location, you will determine the optimal energy usage when taking into consideration costs and comfortability.
    
    Given the recent energy data provided and weather data for the upcoming {predict_string}, generate a prediction for energy consumption for this residential building for the upcoming {predict_string}

    Here is the energy data in CSV format. If negative values are present it means that more solar energy is being produced than the energy consumed:

    {csv_string}

    Here is the weather data for the location of the residential building for the next {predict_string}

    {weather}

    Please output the generated prediction in the form of text, specifically the energy predicted for each hour for the upcoming {predict_string}.

    Afterwards, analyze the energy data provided previously and identify any irregularities or inefficiencies in the energy consumption. Emphasize patterns in specfic time ranges within the dataset.

    Then, provide recommendations to optimize energy usage based on the prediction, and take into account the weather forecast for personalized recommendations.
    """
    print(user_message)
    chatgpt_response = chat_with_chatGPT(user_message)
    return jsonify({'response': chatgpt_response}), 200

def chat_with_chatGPT(prompt):
    model = "gpt-4-turbo"
    openai.api_key = "sk-proj-zfZq8suoT0gfsWt4LakVT3BlbkFJP6VmY4fLs0p3KeOrKZoD"
    response = openai.chat.completions.create(
        model=model,
        messages=[{'role': 'user', "content": prompt}],
        max_tokens=4096
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

@app.route('/forecasts', methods=['POST'])
def forecasts():
    location = request.json.get('location')
    print("Location: ", location)
    latitude, longitude = get_coords(location)
    grid_id, grid_x, grid_y = get_nws_gridpoints(latitude, longitude)
    forecast = get_weekly_forecast(grid_id, grid_x, grid_y)
    forecasts_array = [] #array of strings
    for i in range(14):
        if (i == 0):
            continue
        if (i % 2 == 1): #skips night forecast
            continue
        print("Forecast for the day: " + forecast[i]['detailedForecast'])
        forecasts_array.append(forecast[i]['detailedForecast'])
    print(forecasts_array)
    return jsonify({'forecasts': forecasts_array}), 200

# @app.route('/location', methods=['POST'])
def weather_data(location, length):
    # location = request.json.get('location')
    session['location_string'] = location
    print("THIS IS SESSION DATA FOR LOCATION STRING" + session['location_string'])
    latitude, longitude = get_coords(location)
    print("Latitude: ", latitude, "Longitude: ", longitude)
    grid_id, grid_x, grid_y = get_nws_gridpoints(latitude, longitude)
    print("Grid ID: ", grid_id, "Grid X: ", grid_x, "Grid Y: ", grid_y)
    forecast = get_weekly_forecast(grid_id, grid_x, grid_y)
    weather_string = ""
    for i in range(length*2): #prints out morning and night forecast for the next 7 days
        print("Date: " + forecast[i]['name'])
        weather_string += "Date: " + forecast[i]['name'] + "\n"
        print("Forecast for the day: " + forecast[i]['detailedForecast'])
        weather_string += "Forecast for the day: " + forecast[i]['detailedForecast'] + "\n"
    session['weather'] = weather_string
    print("THIS IS SESSION DATA FOR WEATHER STRING" + session['weather'])
    
    # return jsonify({'message': 'Weather has been forecasted'}), 200
    return weather_string

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': "Welcome to BuildSmart-ToolKit! We are here to help you save energy."}), 200


@app.route('/predict', methods=['POST'])
def predict():
    return jsonify({'message': 'We are predicting your energy consumption now'})

if __name__ == '__main__':
    app.run(debug=True)

