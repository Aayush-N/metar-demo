from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
		HTTP_200_OK,
		HTTP_400_BAD_REQUEST
	)

from config.settings import CACHE_TTL
from .helpers import celcius_to_fahrenheit, cloud_dict, weather_dict

import requests
import re

class StatusCheck(APIView):
	"""
	Returns a response to ensure the system is working fine
	"""

	def get(self, request, format=None):
		"""
		Return a health check response.
		"""
		response_data = {'data': 'pong'}
		return Response(response_data, status=HTTP_200_OK)	



class WeatherCheck(APIView):
	"""
	Returns the decoded version of the METAR report
	data from the API. Parameters:

	scode (Required - four character station code)

	nocache (Optional - set using 1/yes/true/t)
	"""

	def get(self, request, format=None):
		response_data = {}
		station_code = self.request.query_params.get('scode')
		nocache = self.request.query_params.get('nocache', False)

		if nocache:
			# check if string passed to nocache is truthy or not
			# supports yes, true, t and 1 as truth values
			if nocache.lower() in ("yes", "true", "t", "1"):
				nocache = True
			else:
				nocache = False

		# if station code is provided
		if station_code:
			if station_code in cache and not nocache:
				# if data is cached and nocache is set to False, retrieve from cache
				response_data = cache.get(station_code)
				response_data['cached'] = True
				return Response(response_data, status=HTTP_200_OK)	
			else:
				# make a call to the metar API to get data
				metar_response = requests.get('https://tgftp.nws.noaa.gov/data/observations/metar/stations/{}.TXT'.format(station_code))
				
				# if invalid scode is provided, response contains 404 not found text
				if '404 Not Found' not in metar_response.text: 
					data_list = metar_response.text.split()

					# add observation time to response
					response_data['last_observation'] = "{} at {} UTC".format(data_list[0], data_list[1])
					# add station code to response
					response_data['station'] = data_list[2]

					# start iteration from the 4th datapoint as first 3 are already decoded
					for data in data_list[3:-1]:

						# Wind 
						# can be inferred by checking if the datapoint ends with KT
						if data.endswith('KT'):
							
							# wind data can contain G (gusts) so split by G and KT
							wind_list = re.split('KT|G', data)

							if len(wind_list) == 3:
								# condition when the datapoint contains gusts
								wind = 'Direction of {} at {} knots gusting to {} knots'.format(
									wind_list[0][0:3], wind_list[0][3:5], wind_list[1])
							else:
								# general condition when datapoint doesn't contain gusts
								wind = 'Direction of {} at {} knots'.format(wind_list[0][0:3], wind_list[0][3:5])

							response_data['wind'] = wind
							continue
						
						# Visibility
						# check if any datapoint ends with either SM or is a 4 digit number 
						# as intl stations use 4 digit metres representation
						if data.endswith('SM') or re.search("^\d{4}$", data):
							if data.endswith('SM'):
								response_data['visibility'] = data[0:-2] + ' statute miles'
							else:
								response_data['visibility'] = data + ' metres'
							continue

						# Temperature and dewpoint
						# search if any data point matches the required format Mdd/Mdd or dd/dd
						temperature_dewpoint = re.search("^[0-9M]*/[0-9M]*$", data)
						if temperature_dewpoint:
							temperature_dewpoint_list = (temperature_dewpoint.string).split('/')
							
							# check if negative temperature
							if temperature_dewpoint_list[0].upper().startswith('M'):
								# convert M to negative sign
								temperature = "-{}".format(temperature_dewpoint_list[0].split('M')[1])
							else:
								temperature = temperature_dewpoint_list[0]

							# check if negative temperature
							if temperature_dewpoint_list[1].upper().startswith('M'):
								# convert M to negative sign
								dewpoint = "-{}".format(temperature_dewpoint_list[1].split('M')[1])
							else:
								dewpoint = temperature_dewpoint_list[1]

							response_data['temperature_celcius'] = int(temperature)
							response_data['temperature_fahrenheit'] = celcius_to_fahrenheit(temperature)
							response_data['dewpoint_celcius'] = int(dewpoint)
							response_data['dewpoint_fahrenheit'] = celcius_to_fahrenheit(dewpoint)
							continue


						# Clouds
						# check if current datapoint value exists in our clouds dictionary
						# most times cloud data has numbers appended, disregard them
						if cloud_dict.get(data[0:3]):
							clouds_data_present = True
							response_data['clouds'] = cloud_dict[data[0:3]]
							continue
						elif data == 'CAVOK':
							clouds_data_present = True
							response_data['clouds'] = cloud_dict['CAVOK']
							continue
						else:
							pass

						# Weather
						# check if current datapoint value exists in our weather dictionary
						weather_data = data[0:3] in weather_dict.keys()
						if weather_data:
							response_data['weather'] = weather_dict[data[0:3]]
							continue

					# set in cache
					cache.set(station_code, response_data, timeout=CACHE_TTL)
					return Response(response_data, status=HTTP_200_OK)	
				else:
					# case when the station code provided isn't found in the metar API 
					invalid_station_msg = {"data": "Requested station not found."}
					return Response(invalid_station_msg, status=HTTP_400_BAD_REQUEST)	
				
		else:
			# case when the station code parameter isn't provided
			return Response({"data": "Please specify Station Code using the scode parameter."}, status=HTTP_400_BAD_REQUEST)


