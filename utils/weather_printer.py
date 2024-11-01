import datetime
from location_weather import LocationWeather

class WeatherPrinter:
  def __init__(self):
    location_weather = LocationWeather()
    self.weather_data = location_weather.get_weather()

  def format_weather_data(self):
    weather_data_next_3_days = []
    day_after_tomorrow = datetime.date.today() + datetime.timedelta(2)

    for data in self.weather_data['properties']['timeseries']:
      # divide date and time into different strings
      date = data['time'].split('T')[0]
      time = data['time'].split('T')[1].split('Z')[0]
      temperature = data['data']['instant']['details']['air_temperature']

      if 'next_1_hours' in data['data']:
        details = data['data']['next_1_hours']['summary']['symbol_code']
      elif 'next_6_hours' in data['data']:
        details = data['data']['next_6_hours']['summary']['symbol_code']
      elif 'next_12_hours' in data['data']:
        details = data['data']['next_12_hours']['summary']['symbol_code']
      else:
        details = 'weather details not found from the data'

      # add only the data containing these times to the list
      if time == '09:00:00' or time == '12:00:00' or time == '18:00:00' or time == '00:00:00':
        formatted_date = date.split('-')
        formatted_date.reverse()
        formatted_time = time.split(':')

        weather_data_next_3_days.append({
          'date': formatted_date[0] + '.' + formatted_date[1] + '.' + formatted_date[2],
          'time': formatted_time[0] + '.' + formatted_time[1],
          'temperature': temperature,
          'details': details
        })

      # convert the date string into a datetime object for comparison
      date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
      if date_obj > day_after_tomorrow:
        break

    return weather_data_next_3_days

  def print_data(self):
    weather_data = self.format_weather_data()
    # track the current date
    current_date = None
    
    for data in weather_data: 
      if data['date'] != current_date:
        print(data['date'])
        current_date = data['date']

      print(' ', data['time'])
      print(' ', data['temperature'], '°C', end='')
      print('', data['details'])
      print('')
