from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class PingTest(APITestCase):
	def test_ping_service(self):
		'''
		Ensure we receieve a pong when we ping
		'''
		url = reverse('api:staus_check_api')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, {'data': 'pong'})


class MetarInfoTest(APITestCase):
	def test_no_station_code(self):
		'''
		Ensure that on providing no station code, error is handled
		'''
		url = reverse('api:weather_check_api')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response.data, {'data': 'Please specify Station Code using the scode parameter.'})

	def test_invalid_station_code(self):
		'''
		Ensure that on providing an invalid station code, error is handled
		'''
		url = reverse('api:weather_check_api')
		response = self.client.get(url, {'scode': 'AAAAAA'})
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response.data, {'data': 'Requested station not found.'})

	def test_caching_when_nocache_set(self):
		'''
		Ensure cached request is not served when nocache is set
		'''
		url = reverse('api:weather_check_api')
		response = self.client.get(url, {'scode': 'KHUL', 'nocache': 1})
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertFalse('cached' in response.data)

	def test_caching_when_nocache_not_set(self):
		'''
		Ensure caching is working when nocache is not set
		'''
		url = reverse('api:weather_check_api')
		add_to_cache = self.client.get(url, {'scode': 'KHUL'})
		response = self.client.get(url, {'scode': 'KHUL'})
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertTrue('cached' in response.data)

	def test_correct_sample_request(self):
		'''
		Ensure a correct station code request is working fine
		'''
		url = reverse('api:weather_check_api')
		response = self.client.get(url, {'scode': 'KHUL'})
		self.assertEqual(response.status_code, status.HTTP_200_OK)


