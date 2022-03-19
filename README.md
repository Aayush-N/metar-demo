
# METAR Report Demo

Decode and retrieve data from a METAR report provided by the National Weather Service API in realtime

Does not use any METAR decoding module

Uses redis to cache results for 5 minutes


## API Reference

#### Get health check

```http
  GET /metar/ping
```

Returns `{'data': 'pong'}`

#### Get weather info

```http
  GET /metar/info/?scode=${scode}&nocache=${nocache}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `scode`      | `string` | **Required**. 4 character station code of the weather station <br/> we intend to get the METAR report from |
| `nocache`      | `string` | *Optional*. Set using 1/yes/true/T if the user wishes to get fresh data  |

If station exists, returns decoded weather response. Example:

`{
    "last_observation": "2022/03/19 at 10:53 UTC",
    "station": "KHUL",
    "wind": "Direction of 000 at 00 knots",
    "visibility": "10 statue miles",
    "clouds": "Overcast",
    "temperature_celcius": -1,
    "temperature_fahrenheit": 30.2,
    "dewpoint_celcius": -2,
    "dewpoint_fahrenheit": 28.4,
    "cached": true
}`

## Demo

Accessible at: http://172.105.63.176


## Run Locally

Clone the project

```bash
  git clone https://github.com/Aayush-N/metar-demo
```

Go to the metar-demo

```bash
  cd metar-demo
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Run migrations 

```bash
  python manage.py migrate
```

Start the server

```bash
  python manage.py runserver
```

Run test cases

```bash
  python manage.py test
```
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DJANGO_DEBUG`

`SECRET_KEY`


## Tech Stack

Django, Django REST Framework, Redis

National Weather Service API

