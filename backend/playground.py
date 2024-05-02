import openai
import os
import requests
import math
import csv
from geopy.geocoders import Nominatim
import certifi #for SSL certificate verification for MacOS

# Create an instance of the OpenAI class

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

if __name__ == "__main__": #if run from terminal

    #testing will delete this section later
        # Usage Example: "New York City, NY"
    location = input("Enter your location [City, State]: ")

    latitude, longitude = get_coords(location)
    print("Latitude: ", latitude, "Longitude: ", longitude)
    grid_id, grid_x, grid_y = get_nws_gridpoints(latitude, longitude)
    print("Grid ID: ", grid_id, "Grid X: ", grid_x, "Grid Y: ", grid_y)
    forecast = get_weekly_forecast(grid_id, grid_x, grid_y)
    # print(forecast)
    for i in range(14): #prints out morning and night forecast for the next 7 days
        print("Date: ", forecast[i]['name'])
        print("Forecast for the day: ", forecast[i]['detailedForecast'])

    # #end of testing

    # # Provide context message to API on startup
    # contextMessage = "You are an energy predictor trying to predict and minimize energy usage of a residential building given hourly or daily energy consumption data in kWhs, as well as the location of the building."
    # + "You will be predicting energy usage for either the following day or week. Based on the provided data and the prediction, you will identify potential flaws in the energy usage and provide potential solutions to conserve energy." 
    # + "Afterwards, using the weather data associated with the location, you will determine the optimal energy usage when taking into consideration costs and comfortability."
    # establishContext = chat_with_chatGPT(contextMessage)
    # print(establishContext)
    
    
    # # prompt user to input location, csv, prediction time

    # # Usage Example: "New York City, NY"
    # location = input("Enter your location [City, State]: ")
    # city=location.split(",")[0]
    # state=location.split(",")[1]
    # latitude, longitude = get_coords(city, state)
    # print("Latitude: ", latitude, "Longitude: ", longitude)

    # # Usage Example: "/user/Julian/Downloads/energy.csv"
    # csv = input("Enter the file path of your energy usage CSV file: ")

    # csv_as_text = ""

    # # Temporary untested CSV to String code
    # with open(csv, 'r') as file:
    #     csv_reader = csv.reader(file)
    #     for row in csv_reader:
    #         csv_as_text += ','.join(row) + '\n'

    # print(csv_as_text)  # Should print out the csv as a string as this format: Column1 Value, Column2 Value\n ...
    

    # # Usage Example: "day"
    # predict_time = input("Predict the following [day/week]: ")

    # # Gather Weather data using user inputted location from API for predict_time
    

    # # Engineer Prompt - Prediction time, past energy data, weather data,
    # # prompt = f"""You are an energy predictor trying to predict and minimize energy usage of a residential building given hourly or daily energy consumption data in kWhs, as well as the location of the building. You will be predicting energy usage for either the following day or week. Based on the provided data and the prediction, you will identify potential flaws in the energy usage and provide potential solutions to conserve energy. Afterwards, using the weather data associated with the location, you will determine the optimal energy usage when taking into consideration costs and comfortability.
    
    # #Given the recent energy data provided and weather data for the upcoming {predict_time}, generate a prediction for energy consumption for this residential building for the upcoming {predict_time}

    # # Here is the energy data in CSV format:

    # # {csv_as_text}

    # # Here is the weather data for the location of the residential building for the next {predict_time}

    # # {weather_data}

    # # Please output the generated prediction in the format of a csv file.
    
    # # Afterwards, analyze the energy data provided previously and identify any irregularities or inefficiencies in the energy consumption.

    # # Then, provide recommendations to optimize energy usage based on the prediction, and take into account the weather forecast for personalized recommendations.
    # # """

    # prompt = f"""Given the recent energy data provided, generate a prediction for energy consumption for this residential building for the upcoming day

    # Here is the energy data in CSV format:

    

    # Please output the generated prediction in the format of a csv file.
    
    # Afterwards, analyze the energy data provided previously and identify any irregularities or inefficiencies in the energy consumption.

    # Then, provide recommendations to optimize energy usage based on the prediction.
    # """      


    # # Provide ChatGPT with our pre-engineered prompt along with our input data
    # prompt = input("Enter Prompt: ")
    # response = chat_with_chatGPT(prompt)
    # print(response)


