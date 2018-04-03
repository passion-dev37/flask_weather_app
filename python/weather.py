#!/usr/bin/python
# ./weather-app/python/weather.py
'''
Module to parse the JSON weather data from forecast.io (darksky.net) and to
make data manipulaions by using Pandas.
'''
import argparse as ag
import datetime as dt
import pandas as pd

import api_requests as dsky

def getCelsiusFromFarenheit(temp_farenheit):
    '''
    Function to convert temperature from farenheit to celsius.
    '''
    temp_celsius = (5/9) * (temp_farenheit - 32)
    return temp_celsius

def getFarenheitFromCelsius(temp_celsius):
    '''
    Function to convert temperature from celsius to farenheit
    '''
    temp_farenheit = ((9/5) * temp_celsius) + 32
    return temp_farenheit

def getHourlyWeatherData(weather_json_dict):
    '''
    Function to parse out the hourly weather data from the JSON object returned
    from the call to the forecast.io API request (object returned as a response,
    which has a json() key with associated data values).
    '''
    hourly_data = weather_json_dict['hourly']['data']
    return hourly_data

def getForecastHourlyTemperatureSeries(hourly_list):
    '''
    Function to parse out and prepare the weather data into a
    pandas.core.series.Series object with weather data as the values
    and formatted (i.e. human-readable) dates as the series indices.

    INPUT:
        1. 'hourly_list'  ::  - List object of the response object returned from
                              the forecast request to the DarkSky API.
                              - For 'forecast' requests --> hourly data is returned
                              for the next days (48 hrs).
                              - Input is a list of dictionary objects, one for
                              each hour in the next 2 days.
    OUTPUT:
        1. 'hourly_series'  ::  - Pandas.core.series.Series object of temperature
                                data fetched from the DarkSky API.
                                - Series constructed from 2 lists; 1 containing
                                the temperture values from the 'hourly_list' input,
                                the other containing human-readable datetimes,
                                also parsed from the 'hourly_list' input.
    '''
    timestamp_series_list, data_series_list = [], []
    for each_hrs_data in hourly_list:
        timestamp_series_list.append(dsky.convertUnixTime2PST(each_hrs_data['time']))
        data_series_list.append(each_hrs_data['temperature'])
    hourly_series = pd.Series(
        data_series_list,
        index = timestamp_series_list,
        name = 'Hourly temperature data series'
    )
    return hourly_series

def saveWeatherData2Csv(save_2_path):
    '''
    Function to save the parsed weather data-series to a directory defined by
    'save_2_path'.
    '''
    pass

if __name__ == '__main__':

    parser = ag.ArgumentParser(
        description = 'Module to parse and visualize weather data from forecast.io'
    )
    parser.add_argument(
        '-a',
        action = 'store',
        type = str,
        help = 'Address to fetch weather data for'
    )
    parser.add_argument(
        '--forecast',
        action = 'store_true',
        default = False,
        help = 'Boolean trigger to print out the details concerning \'forecast\' \
        requests to the DarkSky API.'
    )
    parser.add_argument(
        '--time_machine',
        action = 'store_true',
        default = False,
        help = 'Boolean trigger to print out the details concerning \'time-machine\' \
        requests to DarkSky API.'
    )
    parser.add_argument(
        '--time',
        action = 'store',
        type = str
    )

    args = parser.parse_args()

    if args.forecast and args.a:
        forecast_res = dsky.getForecastDataFromDarkSkyAPI(args.a)
        forecast_data = forecast_res.json()
        hourly = forecast_data['hourly']['data']
        hourly_series = getForecastHourlyTemperatureSeries(hourly)
        print('\nFetching forecast weather data for %s\n(using the DarkSky API)\n' % args.a)
        print(hourly_series)

    elif args.time_machine and args.time and args.a:
        timeMachineReq = dsky.getTimeMachineDataFromDarkSkyAPI(args.a, args.time)
        print('\nFetching time-machine weather data for %s (from %s to %s midnight)\n' % \
              (args.a, dsky.parseDateString2DateTimeObj(args.time), dt.date.today()))
        print(timeMachineReq.json())
