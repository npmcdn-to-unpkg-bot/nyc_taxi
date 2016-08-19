##To execute this script pass start date and end date in the format YYYY-MM-DD 
##The script will output a csv file that contains hourly weather data between start date and end date
import sys
import datetime as dt
import pandas as pd
import forecastio

##Declare API and latitude, longitude for Central Park
api_key = '421847f3f25c45d05f93a8f063cf9147'
central_park_lat = 40.7764
central_park_lon = -73.9676

##Function to create an empty pandas dataframe with request start date and end date as input
##Creates dataframe with every hour and day between start and end date
def create_pddf(start_date, end_date):
    column = ['DateTime', 'Temperature', 'Humidity', 'PrecipIntensity', 'PrecipType']
    index = pd.date_range(start_date, end_date, freq='H', closed='left')
    return pd.DataFrame(index=index, columns=column)

##This is the main function that obtains the historical weather data by date
def get_weather(history_date, weather_history):
    forecast = forecastio.load_forecast(api_key, central_park_lat, central_park_lon, time=history_date)
    byHour = forecast.hourly()
    
    ##Break-up the parts of the date
    year = history_date.year
    month = history_date.month
    day = history_date.day
    hour = 0
    
    ##Start loop for data extracted for each hour of the day
    for hourlyData in byHour.data:
        if hour < 24: ##Day-light savings
            datetime_index = dt.datetime(year, month, day, hour)
            weather_history.loc[datetime_index]['DateTime'] = datetime_index
            try:
                weather_history.loc[datetime_index]['Temperature'] = hourlyData.temperature
            except:
                pass
            try:
                weather_history.loc[datetime_index]['Humidity'] = hourlyData.humidity
            except:
                pass
            try:
                weather_history.loc[datetime_index]['PrecipIntensity'] = hourlyData.precipIntensity
                if hourlyData.precipIntensity != 0:
                    weather_history.loc[datetime_index]['PrecipType'] = hourlyData.precipType
            except: 
                pass
        hour += 1

    return weather_history

if __name__ == '__main__':
    if len(sys.argv) == 3:
        start_date = sys.argv[1]
        end_date = sys.argv[2]
        filename = 'Weather_history-' + start_date + '_' + end_date
        try:
            weather_history = create_pddf(start_date, end_date)
            if start_date < end_date:
                ##start loop for each day
                for date in pd.date_range(start_date, end_date, freq='D', closed='left'):
                    weather_history = get_weather(date, weather_history)
                weather_history.to_csv(filename, index=False) ##output csv
            else:
                print 'First date should be earlier than the second date'
        except:
            print 'Please pass two dates in the format of YYYY-MM-DD'
    else:
        print 'Please pass two dates in the format of YYYY-MM-DD'