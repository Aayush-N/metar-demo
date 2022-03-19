'''
Contains helper functions and dicts
to make code more modular
'''

def celcius_to_fahrenheit(celcius):
	'''
	Converts integer valued celcius to fahrenheit
	Returns a floating value with 2 decimal places
	'''
	fahrenheit = (9 * int(celcius)/5) + 32
	return float("{:.2f}".format(fahrenheit))


cloud_dict = {
	'SKC' :'Sky clear',
	'CLR' :'No clouds detected below 12000 feet)',
	'FEW' :'Few',
	'SCT' :'Scattered',
	'BKN' :'Broken',
	'OVC' :'Overcast',
	'CAVOK': 'No significant weather, the visibility is 10 km or greater, and the ceilings are greater than 5,000 ft.'
}

weather_dict = {
	'DZ': 'Drizzle',
	'DZ': 'Drizzle BR Mist, vis. ≥ 5/8SM DS Dust Storm',
	'GR':'Hail, diam. ≥ 5mm (.25") (or ≥ 1000m)',
	'FC': 'Funnel cloud(s)',
	'GS':'Small Hail / Snow Pellets, DU Widespread Dust e.g., tornado diam. < 5mm (.25")',
	'FG': 'Fog, vis. < 5/8SM or waterspout',
	'IC':'Ice Crystals (or ≥ 1000m) PO Well-developed',
	'PL':'Ice Pellets',
	'FU':'Smoke dust/sand whirls',
	'RA': 'Rain',
	'HZ': 'Haze',
	'SQ': 'Squalls',
	'SG' :'Snow Grains',
	'PY': 'Spray',
	'SS' :'Sandstorm',
	'SN' :'Snow',
	'SA' :'Sand',
	'UP': 'Unknown Precipitation',
	'VA': 'Volcanic Ash',
}